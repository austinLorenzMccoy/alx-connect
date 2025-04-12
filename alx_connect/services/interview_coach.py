import logging
from datetime import datetime, timedelta
from typing import Dict, List
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from ..models.chat import Message, MessageRole, ConversationState
from ..config.config import INTERVIEW_COACH_CONFIG, GROQ_MODEL_NAME, GROQ_API_KEY

class InterviewCoach:
    def __init__(self):
        self.setup_logging()
        self.conversations: Dict[str, ConversationState] = {}
        self.llm = ChatGroq(
            model_name=GROQ_MODEL_NAME,
            api_key=GROQ_API_KEY,
            temperature=0.7
        )
        self.initialize_rag()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def initialize_rag(self):
        self.embeddings = HuggingFaceEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vectorstore = FAISS.from_texts(
            ["Initial empty document"],
            self.embeddings
        )

    def process_csv_data(self, csv_data: List[Dict[str, str]]) -> List[str]:
        processed_texts = []
        for row in csv_data:
            text = f"""
            Question: {row.get('question', '')}
            Answer: {row.get('answer', '')}
            Category: {row.get('category', '')}
            Difficulty: {row.get('difficulty', '')}
            """
            processed_texts.append(text)
        return processed_texts

    def create_rag_chain(self) -> RetrievalQA:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert interview coach. Use the following context to help answer the question. If you don't know the answer, say you don't know.\n\nContext: {context}"),
            ("human", "{question}")
        ])

        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(),
            chain_type_kwargs={
                "prompt": prompt,
                "document_variable_name": "context"
            }
        )

    def clean_response(self, response: str) -> str:
        # Remove any markdown code blocks
        response = response.replace("```", "")
        # Remove any HTML tags
        response = response.replace("<", "").replace(">", "")
        return response.strip()

    def get_conversation_context(self, conversation_id: str, context_window: int = INTERVIEW_COACH_CONFIG["context_window"]) -> str:
        if conversation_id not in self.conversations:
            return ""
        
        messages = self.conversations[conversation_id].messages
        recent_messages = messages[-context_window:]
        return "\n".join([f"{msg.role}: {msg.content}" for msg in recent_messages])

    def add_message_to_conversation(self, conversation_id: str, role: MessageRole, content: str):
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationState()
        
        message = Message(role=role, content=content)
        self.conversations[conversation_id].messages.append(message)
        self.conversations[conversation_id].last_activity = datetime.now()

    def clean_inactive_conversations(self):
        current_time = datetime.now()
        inactive_threshold = timedelta(seconds=INTERVIEW_COACH_CONFIG["max_conversation_age"])
        
        inactive_ids = [
            conv_id for conv_id, state in self.conversations.items()
            if current_time - state.last_activity > inactive_threshold
        ]
        
        for conv_id in inactive_ids:
            del self.conversations[conv_id]
            self.logger.info(f"Cleaned up inactive conversation: {conv_id}") 