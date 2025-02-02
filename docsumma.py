import os
import tempfile
import shutil
from pathlib import Path
from IPython.display import Markdown, display

# Docling imports
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
    SimplePipeline,
)

# LangChain imports
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# It seems that there something wrong with OpenMP in Windows. This is a bad workaround.
# Check if we are running on Windows
if os.name == "nt":
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def get_document_format(file_path) -> InputFormat:
    """Determine the document format based on file extension"""
    try:
        file_path = str(file_path)
        extension = os.path.splitext(file_path)[1].lower()

        format_map = {
            ".pdf": InputFormat.PDF,
            ".docx": InputFormat.DOCX,
            ".doc": InputFormat.DOCX,
            ".pptx": InputFormat.PPTX,
            ".html": InputFormat.HTML,
            ".htm": InputFormat.HTML,
        }
        return format_map.get(extension, None)
    except:
        return "Error in get_document_format: {str(e)}"


def convert_document_to_markdown(doc_path) -> str:
    """Convert document to markdown using simplified pipeline"""
    try:
        # Convert to absolute path string
        input_path = os.path.abspath(str(doc_path))
        print(f"Converting document: {doc_path}")

        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy input file to temp directory
            temp_input = os.path.join(temp_dir, os.path.basename(input_path))
            shutil.copy2(input_path, temp_input)

            # Configure pipeline options
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = False  # Disable OCR temporarily
            pipeline_options.do_table_structure = True

            # Create converter with minimal options
            converter = DocumentConverter(
                allowed_formats=[
                    InputFormat.PDF,
                    InputFormat.DOCX,
                    InputFormat.HTML,
                    InputFormat.PPTX,
                ],
                format_options={
                    InputFormat.PDF: PdfFormatOption(
                        pipeline_options=pipeline_options,
                    ),
                    InputFormat.DOCX: WordFormatOption(pipeline_cls=SimplePipeline),
                },
            )

            # Convert document
            print("Starting conversion...")
            conv_result = converter.convert(temp_input)

            if not conv_result or not conv_result.document:
                raise ValueError(f"Failed to convert document: {doc_path}")

            # Export to markdown
            print("Exporting to markdown...")
            md = conv_result.document.export_to_markdown()

            # Create output path
            output_dir = os.path.dirname(input_path)
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            md_path = os.path.join(output_dir, f"{base_name}_converted.md")

            # Write markdown file
            print(f"Writing markdown to: {base_name}_converted.md")
            with open(md_path, "w", encoding="utf-8") as fp:
                fp.write(md)

            return md_path
    except:
        return f"Error converting document: {doc_path}"


def setup_qa_chain(
    markdown_path: Path,
    embeddings_model_name: str = "nomic-embed-text:latest",
    model_name: str = "granite3.1-dense:8b",
):
    """Set up the QA chain for document processing"""
    # Load and split the document
    try:
        loader = UnstructuredMarkdownLoader(str(markdown_path))
        documents = loader.load()
    except TypeError as tt:
        print(f"Error loading documents: {tt}")
        return None

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, length_function=len
    )
    texts = text_splitter.split_documents(documents)
    # texts= documents

    # Create embeddings and vector store
    embeddings = OllamaEmbeddings(model=embeddings_model_name)
    vectorstore = FAISS.from_documents(texts, embeddings)

    # Initialize LLM
    llm = OllamaLLM(model=model_name, temperature=0)

    # Set up conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history", output_key="answer", return_messages=True
    )

    # Create the chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
        memory=memory,
        return_source_documents=True,
    )

    return qa_chain


def ask_question_ipython(qa_chain, question: str):
    """Ask a question and display the answer"""
    result = qa_chain.invoke({"question": question})
    display(Markdown(f"**Question:** {question}\n\n**Answer:** {result['answer']}"))


def ask_question(qa_chain, question: str):
    """Ask a question and display the answer"""
    result = qa_chain.invoke({"question": question})
    # display(Markdown(f"**Question:** {question}\n\n**Answer:** {result['answer']}"))
    # print(f"Question: {question}\nAnswer: {result['answer']}\n\n")
    return result


def main():

    files = os.listdir("data")

    for file in files:
        doc_path = Path("data").joinpath(file)  # Replace with your document path

        # Check format and process
        doc_format = get_document_format(doc_path)
        if doc_format:
            md_path = convert_document_to_markdown(doc_path)
            qa_chain = setup_qa_chain(md_path)

            # Example questions
            questions = [
                "What is the main topic of this document?",
                "What are the key points discussed?",
                "Can you summarize the conclusions?",
            ]

            # doc_answer = Path("data").joinpath(f"answer_{file}")
            # with open(doc_answer, "a") as ff:
            #     for question in questions:
            #         result = ask_question(qa_chain, question)
            #         ff.write(question + "\n")
            #         ff.write(result["answer"])
        else:
            print(f"Unsupported document format: {doc_path.suffix}")


if __name__ == "__main__":
    main()
