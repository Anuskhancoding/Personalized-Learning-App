

# import streamlit as st
# import requests

# # Base URL for RAGFlow API
# BASE_URL = "http://127.0.0.1"  # Update with your server URL
# API_KEY = "ragflow-czMGFmN2I4YmRkYzExZWY5Yjg5MDI0Mm"
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# st.title("RAGFlow API Integration")

# # Sidebar Navigation
# st.sidebar.title("Navigation")
# options = st.sidebar.radio("Choose a task:", ["Create Dataset", "Upload Document", "Chat Assistant"])

# # Dataset Creation Section
# if options == "Create Dataset":
#     st.header("Create a New Dataset")

#     # Dataset Details
#     dataset_name = st.text_input("Dataset Name", placeholder="Enter a unique dataset name")
#     language = st.selectbox("Language", ["English", "Chinese"])
#     embedding_model = st.text_input("Embedding Model", placeholder="e.g., BAAI/bge-large-zh-v1.5")
#     permission = st.selectbox("Permission", ["me", "team"])
#     chunk_method = st.selectbox(
#         "Chunk Method",
#         [
#             "naive", "manual", "qa", "table", "paper", "book", "laws",
#             "presentation", "picture", "one", "knowledge_graph", "email"
#         ]
#     )

#     if st.button("Create Dataset"):
#         # Prepare the request payload
#         payload = {
#             "name": dataset_name,
#             "language": language,
#             "embedding_model": embedding_model,
#             "permission": permission,
#             "chunk_method": chunk_method,
#         }

#         # API Call
#         response = requests.post(f"{BASE_URL}/api/v1/datasets", json=payload, headers=HEADERS)
#         if response.status_code == 200 and response.json().get("code") == 0:
#             st.success("Dataset created successfully!")
#         else:
#             st.error(f"Failed to create dataset: {response.json().get('message')}")

# # Document Upload Section
# elif options == "Upload Document":
#     st.header("Upload a Document to a Dataset")

#     # Fetch and List Datasets
#     response = requests.get(f"{BASE_URL}/api/v1/datasets", headers=HEADERS)
    
#     if response.status_code == 200 and response.json().get("code") == 0:
#         datasets = response.json().get("data")
#         dataset_names = [dataset["name"] for dataset in datasets]
        
#         # Dropdown for dataset selection by name
#         dataset_name = st.selectbox("Select Dataset", dataset_names)

#         if dataset_name:
#             # Check if dataset exists by name
#             selected_dataset = next((dataset for dataset in datasets if dataset["name"] == dataset_name), None)

#             if selected_dataset:
#                 # Get the dataset ID of the selected dataset
#                 dataset_id = selected_dataset["id"]

#                 # File Upload
#                 uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"])

#                 # Prepare the parser configuration for PDFs
#                 parser_config = {
#                     "chunk_token_count": 128,  # default chunk size
#                     "layout_recognize": True,  # Try recognizing layout
#                     "html4excel": False,  # Don't convert Excel to HTML
#                     "delimiter": "\n!?;。；！？",  # Default delimiters
#                     "task_page_size": 12,  # For PDF only, adjust if needed
#                     "raptor": {"use_raptor": False}  # Default raptor config
#                 }

#                 if st.button("Upload Document"):
#                     if uploaded_file:
#                         # Handle the file upload correctly
#                         files = {"file": uploaded_file}

#                         # Update payload with proper chunking method and parser config
#                         payload = {
#                             "chunk_method": "naive",  # Use naive or "manual" chunking method
#                             "parser_config": parser_config
#                         }

#                         try:
#                             response = requests.post(
#                                 f"{BASE_URL}/api/v1/datasets/{dataset_id}/documents", 
#                                 headers={"Authorization": f"Bearer {API_KEY}"}, 
#                                 files=files, 
#                                 data=payload
#                             )
#                             if response.status_code == 200 and response.json().get("code") == 0:
#                                 st.success("File uploaded successfully!")

#                                 # Fetch the uploaded documents for this dataset
#                                 document_list_response = requests.get(
#                                     f"{BASE_URL}/api/v1/datasets/{dataset_id}/documents",
#                                     headers={"Authorization": f"Bearer {API_KEY}"}
#                                 )

#                                 if document_list_response.status_code == 200 and document_list_response.json().get("code") == 0:
#                                     documents = document_list_response.json().get("data").get("docs")
#                                     document_ids = [doc["id"] for doc in documents]
#                                     document_names = [doc["name"] for doc in documents]

#                                     # Dropdown for selecting a document to parse
#                                     document_name_to_parse = st.selectbox("Select a document to parse", document_names)

#                                     if document_name_to_parse:
#                                         selected_document = next((doc for doc in documents if doc["name"] == document_name_to_parse), None)
#                                         document_id_to_parse = selected_document["id"]

#                                         # Button to trigger the parsing of the selected document
#                                         if st.button(f"Parse '{document_name_to_parse}'"):
#                                             parse_payload = {
#                                                 "document_ids": [document_id_to_parse]
#                                             }
#                                             parse_response = requests.post(
#                                                 f"{BASE_URL}/api/v1/datasets/{dataset_id}/chunks",
#                                                 json=parse_payload,
#                                                 headers={"Authorization": f"Bearer {API_KEY}"}
#                                             )

#                                             if parse_response.status_code == 200 and parse_response.json().get("code") == 0:
#                                                 st.success("Document is being parsed!")
#                                             else:
#                                                 st.error(f"Failed to parse document: {parse_response.json().get('message')}")
#                                         else:
#                                             st.warning("Please select a document to parse.")
#                             else:
#                                 st.error(f"Failed to upload file: {response.json().get('message')}")
#                         except requests.exceptions.RequestException as e:
#                             st.error(f"An error occurred while uploading the file: {e}")
#                     else:
#                         st.warning("Please upload a file.")
#             else:
#                 st.error(f"Dataset with the name '{dataset_name}' does not exist.")
#         else:
#             st.warning("Please select a dataset.")
#     else:
#         st.error("Failed to fetch datasets. Please check your API connection.")

# # Chat Assistant Section
# elif options == "Chat Assistant":
#     st.header("Chat with Assistant")

#     # Chat Interaction
#     chat_id = st.text_input("Chat Assistant ID", placeholder="Enter the Chat Assistant ID")
#     user_query = st.text_area("Your Query", placeholder="Type your question here...")

#     if st.button("Ask Assistant"):
#         if chat_id and user_query:
#             payload = {
#                 "question": user_query,
#                 "stream": False
#             }
#             response = requests.post(
#                 f"{BASE_URL}/api/v1/chats/{chat_id}/completions", json=payload, headers=HEADERS
#             )
#             if response.status_code == 200 and response.json().get("code") == 0:
#                 st.write(response.json().get("data").get("answer"))
#             else:
#                 st.error(f"Failed to get response: {response.json().get('message')}")
#         else:
#             st.warning("Please provide both Chat Assistant ID and a query.")













# import streamlit as st
# import requests
# import json

# API_URL = "http://127.0.0.1/api/v1"
# API_KEY = "ragflow-czMGFmN2I4YmRkYzExZWY5Yjg5MDI0Mm"
# HEADERS = {
#     'Authorization': f'Bearer {API_KEY}',
#     'Content-Type': 'application/json'
# }

# # Function to create a dataset
# def create_dataset():
#     st.subheader("Create Dataset")
#     name = st.text_input("Dataset Name")
#     description = st.text_input("Description")
#     language = st.selectbox("Language", ["English", "Chinese"])
#     embedding_model = st.text_input("Embedding Model")
#     permission = st.selectbox("Permission", ["me", "team"])
#     chunk_method = st.selectbox("Chunk Method", ["naive", "manual", "qa", "table", "paper", "book", "laws", "presentation", "picture", "one", "knowledge_graph"])

#     if st.button("Create Dataset"):
#         payload = {
#             "name": name,
#             "description": description,
#             "language": language,
#             "embedding_model": embedding_model,
#             "permission": permission,
#             "chunk_method": chunk_method
#         }

#         response = requests.post(f'{API_URL}/datasets', headers=HEADERS, data=json.dumps(payload))
#         data = response.json()
#         if response.status_code == 200 and data['code'] == 0:
#             st.success(f"Dataset '{name}' created successfully!")
#         else:
#             st.error(f"Error: {data.get('message', 'Unknown error')}")

# # Function to search and list datasets by name
# def list_datasets_by_name(name_filter):
#     params = {"name": name_filter}
#     response = requests.get(f'{API_URL}/datasets', headers=HEADERS, params=params)
#     data = response.json()
#     if response.status_code == 200 and data['code'] == 0:
#         return data.get('data', [])
#     return []

# # Function to upload documents to a dataset
# def upload_documents():
#     st.subheader("Upload Documents to Dataset")
#     dataset_name = st.text_input("Dataset Name")  # Search dataset by name
#     uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

#     if st.button("Upload Documents"):
#         if not dataset_name:
#             st.error("Please enter a dataset name.")
#             return

#         # Search for the dataset by name
#         datasets = list_datasets_by_name(dataset_name)
#         if datasets:
#             dataset_id = datasets[0]['id']  # Assuming the first dataset is the correct one
#             if not uploaded_files:
#                 st.error("Please upload at least one file.")
#                 return

#             # Upload each file to the found dataset
#             for file in uploaded_files:
#                 response = requests.post(
#                     f'{API_URL}/datasets/{dataset_id}/documents',
#                     headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'multipart/form-data'},
#                     files={'file': file}
#                 )
#                 data = response.json()
#                 if response.status_code == 200 and data['code'] == 0:
#                     st.success(f"File '{file.name}' uploaded successfully!")
#                 else:
#                     st.error(f"Error: {data.get('message', 'Unknown error')}")
#         else:
#             st.error("No dataset found with the provided name.")

# # Function to list and parse documents in a dataset
# def list_and_parse_documents():
#     st.subheader("Parse Documents in Dataset")
#     dataset_name = st.text_input("Dataset Name (Search)")  # Search dataset by name

#     if dataset_name:
#         # Search for the dataset by name
#         datasets = list_datasets_by_name(dataset_name)
#         if datasets:
#             dataset = datasets[0]  # Assuming the first dataset is the correct one
#             st.write(f"Found dataset: {dataset['name']} (ID: {dataset['id']})")

#             # Fetch documents for the selected dataset
#             response = requests.get(f'{API_URL}/datasets/{dataset["id"]}/documents', headers=HEADERS)
#             data = response.json()

#             if response.status_code == 200 and data['code'] == 0:
#                 documents = data.get('data', {}).get('docs', [])
#                 if documents:
#                     for doc in documents:
#                         doc_name = doc.get('name', 'No Name')
#                         doc_id = doc.get('id', '')
#                         if st.button(f"Parse '{doc_name}'", key=doc_id):
#                             parse_document(dataset['id'], doc_id)  # Trigger parsing of the document
#                 else:
#                     st.warning("No documents found.")
#             else:
#                 st.error(f"Error: {data.get('message', 'Unknown error')}")
#         else:
#             st.warning("No datasets found matching the name.")
#     else:
#         st.warning("Please enter a dataset name to search.")

# # Function to trigger parsing of a document
# def parse_document(dataset_id, document_id):
#     payload = {"document_ids": [document_id]}
#     response = requests.post(f'{API_URL}/datasets/{dataset_id}/chunks', headers=HEADERS, data=json.dumps(payload))
#     data = response.json()

#     if response.status_code == 200 and data['code'] == 0:
#         st.success(f"Document with ID {document_id} parsed successfully!")
#     else:
#         st.error(f"Error: {data.get('message', 'Unknown error')}")

# # Function to manage datasets
# def manage_datasets():
#     st.subheader("Manage Datasets")
#     name_filter = st.text_input("Dataset Name (Filter)")

#     if st.button("List Datasets"):
#         if name_filter:
#             datasets = list_datasets_by_name(name_filter)
#             if datasets:
#                 for dataset in datasets:
#                     st.write(f"Dataset Name: {dataset['name']}, ID: {dataset['id']}")
#             else:
#                 st.warning("No datasets found.")
#         else:
#             st.warning("Please enter a name to filter datasets.")

# # Main function to handle navigation
# def main():
#     st.title("")
#     menu = ["Create Dataset", "Upload Documents", "Parse Documents", "Manage Datasets"]
#     choice = st.sidebar.selectbox("Select Action", menu)

#     if choice == "Create Dataset":
#         create_dataset()
#     elif choice == "Upload Documents":
#         upload_documents()  # Upload documents to a dataset by name
#     elif choice == "Parse Documents":
#         list_and_parse_documents()  # List documents and parse them by name
#     elif choice == "Manage Datasets":
#         manage_datasets()  # Manage datasets by name

# if __name__ == "__main__":
#     main()





# import streamlit as st
# import requests
# import json

# API_URL = "http://127.0.0.1/api/v1"
# API_KEY = "ragflow-czMGFmN2I4YmRkYzExZWY5Yjg5MDI0Mm"
# HEADERS = {
#     'Authorization': f'Bearer {API_KEY}',
#     'Content-Type': 'application/json'
# }

# # Function to display logo
# def display_logo():
#     # st.image(r"C:\Users\Administrator\Downloads\logo.jpg", width=200)  # Replace with your image URL or path
#     st.image("logo.jpg", width=200)


# # Function to create a dataset
# def create_dataset():
#     display_logo()  # Add the logo to the top of the section
#     st.subheader("Create Dataset")
#     name = st.text_input("Dataset Name")
#     description = st.text_input("Description")
#     language = st.selectbox("Language", ["English", "Chinese"])
#     embedding_model = st.text_input("Embedding Model")
#     permission = st.selectbox("Permission", ["me", "team"])
#     chunk_method = st.selectbox("Chunk Method", ["naive", "manual", "qa", "table", "paper", "book", "laws", "presentation", "picture", "one", "knowledge_graph"])

#     if st.button("Create Dataset"):
#         payload = {
#             "name": name,
#             "description": description,
#             "language": language,
#             "embedding_model": embedding_model,
#             "permission": permission,
#             "chunk_method": chunk_method
#         }

#         response = requests.post(f'{API_URL}/datasets', headers=HEADERS, data=json.dumps(payload))
#         data = response.json()
#         if response.status_code == 200 and data['code'] == 0:
#             st.success(f"Dataset '{name}' created successfully!")
#         else:
#             st.error(f"Error: {data.get('message', 'Unknown error')}")

# # Function to search and list datasets by name
# def list_datasets_by_name(name_filter):
#     params = {"name": name_filter}
#     response = requests.get(f'{API_URL}/datasets', headers=HEADERS, params=params)
#     data = response.json()
#     if response.status_code == 200 and data['code'] == 0:
#         return data.get('data', [])
#     return []

# # Function to upload documents to a dataset
# def upload_documents():
#     display_logo()  # Add the logo to the top of the section
#     st.subheader("Upload Documents to Dataset")
#     dataset_name = st.text_input("Dataset Name")  # Search dataset by name
#     uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

#     if st.button("Upload Documents"):
#         if not dataset_name:
#             st.error("Please enter a dataset name.")
#             return

#         # Search for the dataset by name
#         datasets = list_datasets_by_name(dataset_name)
#         if datasets:
#             dataset_id = datasets[0]['id']  # Assuming the first dataset is the correct one
#             if not uploaded_files:
#                 st.error("Please upload at least one file.")
#                 return

#             # Upload each file to the found dataset
#             for file in uploaded_files:
#                 response = requests.post(
#                     f'{API_URL}/datasets/{dataset_id}/documents',
#                     headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'multipart/form-data'},
#                     files={'file': file}
#                 )
#                 data = response.json()
#                 if response.status_code == 200 and data['code'] == 0:
#                     st.success(f"File '{file.name}' uploaded successfully!")
#                 else:
#                     st.error(f"Error: {data.get('message', 'Unknown error')}")
#         else:
#             st.error("No dataset found with the provided name.")

# # Function to list and parse documents in a dataset
# def list_and_parse_documents():
#     display_logo()  # Add the logo to the top of the section
#     st.subheader("Parse Documents in Dataset")
#     dataset_name = st.text_input("Dataset Name (Search)")  # Search dataset by name

#     if dataset_name:
#         # Search for the dataset by name
#         datasets = list_datasets_by_name(dataset_name)
#         if datasets:
#             dataset = datasets[0]  # Assuming the first dataset is the correct one
#             st.write(f"Found dataset: {dataset['name']} (ID: {dataset['id']})")

#             # Fetch documents for the selected dataset
#             response = requests.get(f'{API_URL}/datasets/{dataset["id"]}/documents', headers=HEADERS)
#             data = response.json()

#             if response.status_code == 200 and data['code'] == 0:
#                 documents = data.get('data', {}).get('docs', [])
#                 if documents:
#                     for doc in documents:
#                         doc_name = doc.get('name', 'No Name')
#                         doc_id = doc.get('id', '')
#                         if st.button(f"Parse '{doc_name}'", key=doc_id):
#                             parse_document(dataset['id'], doc_id)  # Trigger parsing of the document
#                 else:
#                     st.warning("No documents found.")
#             else:
#                 st.error(f"Error: {data.get('message', 'Unknown error')}")
#         else:
#             st.warning("No datasets found matching the name.")
#     else:
#         st.warning("Please enter a dataset name to search.")

# # Function to trigger parsing of a document
# def parse_document(dataset_id, document_id):
#     payload = {"document_ids": [document_id]}
#     response = requests.post(f'{API_URL}/datasets/{dataset_id}/chunks', headers=HEADERS, data=json.dumps(payload))
#     data = response.json()

#     if response.status_code == 200 and data['code'] == 0:
#         st.success(f"Document with ID {document_id} parsed successfully!")
#     else:
#         st.error(f"Error: {data.get('message', 'Unknown error')}")

# # Function to manage datasets
# def manage_datasets():
#     display_logo()  # Add the logo to the top of the section
#     st.subheader("Manage Datasets")
#     name_filter = st.text_input("Dataset Name (Filter)")

#     if st.button("List Datasets"):
#         if name_filter:
#             datasets = list_datasets_by_name(name_filter)
#             if datasets:
#                 for dataset in datasets:
#                     st.write(f"Dataset Name: {dataset['name']}, ID: {dataset['id']}")
#             else:
#                 st.warning("No datasets found.")
#         else:
#             st.warning("Please enter a name to filter datasets.")

# # Main function to handle navigation
# def main():
#     st.title("Personalized Learning ")
#     display_logo()  # Display logo at the top of the app

#     menu = ["Create Dataset", "Upload Documents", "Parse Documents", "Manage Datasets"]
#     choice = st.sidebar.selectbox("Select Action", menu)

#     if choice == "Create Dataset":
#         create_dataset()
#     elif choice == "Upload Documents":
#         upload_documents()  # Upload documents to a dataset by name
#     elif choice == "Parse Documents":
#         list_and_parse_documents()  # List documents and parse them by name
#     elif choice == "Manage Datasets":
#         manage_datasets()  # Manage datasets by name

# if __name__ == "__main__":
#     main()




import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1/api/v1"
API_KEY = "ragflow-czMGFmN2I4YmRkYzExZWY5Yjg5MDI0Mm"
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Function to display logo (only once at the top)
def display_logo():
    st.image(r"C:\\Users\\Administrator\\Downloads\\logo.jpg", width=200)

# Function to create a dataset
def create_dataset():
    st.subheader("Create Dataset")
    name = st.text_input("Dataset Name")
    description = st.text_input("Description")
    language = st.selectbox("Language", ["English", "Chinese"])
    embedding_model = st.text_input("Embedding Model")
    permission = st.selectbox("Permission", ["me", "team"])
    chunk_method = st.selectbox("Chunk Method", ["naive", "manual", "qa", "table", "paper", "book", "laws", "presentation", "picture", "one", "knowledge_graph"])

    if st.button("Create Dataset"):
        payload = {
            "name": name,
            "description": description,
            "language": language,
            "embedding_model": embedding_model,
            "permission": permission,
            "chunk_method": chunk_method
        }

        response = requests.post(f'{API_URL}/datasets', headers=HEADERS, data=json.dumps(payload))
        data = response.json()
        if response.status_code == 200 and data['code'] == 0:
            st.success(f"Dataset '{name}' created successfully!")
        else:
            st.error(f"Error: {data.get('message', 'Unknown error')}")

# Function to search and list datasets by name
def list_datasets_by_name(name_filter):
    params = {"name": name_filter}
    response = requests.get(f'{API_URL}/datasets', headers=HEADERS, params=params)
    data = response.json()
    if response.status_code == 200 and data['code'] == 0:
        return data.get('data', [])
    return []

# Function to upload documents to a dataset
def upload_documents():
    st.subheader("Upload Documents to Dataset")
    dataset_name = st.text_input("Dataset Name")  # Search dataset by name
    uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

    if st.button("Upload Documents"):
        if not dataset_name:
            st.error("Please enter a dataset name.")
            return

        # Search for the dataset by name
        datasets = list_datasets_by_name(dataset_name)
        if datasets:
            dataset_id = datasets[0]['id']  # Assuming the first dataset is the correct one
            if not uploaded_files:
                st.error("Please upload at least one file.")
                return

            # Upload each file to the found dataset
            for file in uploaded_files:
                response = requests.post(
                    f'{API_URL}/datasets/{dataset_id}/documents',
                    headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'multipart/form-data'},
                    files={'file': file}
                )
                data = response.json()
                if response.status_code == 200 and data['code'] == 0:
                    st.success(f"File '{file.name}' uploaded successfully!")
                else:
                    st.error(f"Error: {data.get('message', 'Unknown error')}")
        else:
            st.error("No dataset found with the provided name.")

# Function to list and parse documents in a dataset
def list_and_parse_documents():
    st.subheader("Parse Documents in Dataset")
    dataset_name = st.text_input("Dataset Name (Search)")  # Search dataset by name

    if dataset_name:
        # Search for the dataset by name
        datasets = list_datasets_by_name(dataset_name)
        if datasets:
            dataset = datasets[0]  # Assuming the first dataset is the correct one
            st.write(f"Found dataset: {dataset['name']} (ID: {dataset['id']})")

            # Fetch documents for the selected dataset
            response = requests.get(f'{API_URL}/datasets/{dataset["id"]}/documents', headers=HEADERS)
            data = response.json()

            if response.status_code == 200 and data['code'] == 0:
                documents = data.get('data', {}).get('docs', [])
                if documents:
                    for doc in documents:
                        doc_name = doc.get('name', 'No Name')
                        doc_id = doc.get('id', '')
                        if st.button(f"Parse '{doc_name}'", key=doc_id):
                            parse_document(dataset['id'], doc_id)  # Trigger parsing of the document
                else:
                    st.warning("No documents found.")
            else:
                st.error(f"Error: {data.get('message', 'Unknown error')}")
        else:
            st.warning("No datasets found matching the name.")
    else:
        st.warning("Please enter a dataset name to search.")

# Function to trigger parsing of a document
def parse_document(dataset_id, document_id):
    payload = {"document_ids": [document_id]}
    response = requests.post(f'{API_URL}/datasets/{dataset_id}/chunks', headers=HEADERS, data=json.dumps(payload))
    data = response.json()

    if response.status_code == 200 and data['code'] == 0:
        st.success(f"Document with ID {document_id} parsed successfully!")
    else:
        st.error(f"Error: {data.get('message', 'Unknown error')}")

# Function to manage datasets
def manage_datasets():
    st.subheader("Manage Datasets")
    name_filter = st.text_input("Dataset Name (Filter)")

    if st.button("List Datasets"):
        if name_filter:
            datasets = list_datasets_by_name(name_filter)
            if datasets:
                for dataset in datasets:
                    st.write(f"Dataset Name: {dataset['name']}, ID: {dataset['id']}")
            else:
                st.warning("No datasets found.")
        else:
            st.warning("Please enter a name to filter datasets.")

# Main function to handle navigation
def main():
    st.set_page_config(page_title="Personalized Learning", page_icon=":book:", layout="wide")
    st.title("Personalized Learning")  # Display the app title in large font
    display_logo()  # Display logo only once at the top of the app

    menu = ["Create Dataset", "Upload Documents", "Parse Documents", "Manage Datasets"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Create Dataset":
        create_dataset()
    elif choice == "Upload Documents":
        upload_documents()  # Upload documents to a dataset by name
    elif choice == "Parse Documents":
        list_and_parse_documents()  # List documents and parse them by name
    elif choice == "Manage Datasets":
        manage_datasets()  # Manage datasets by name

if __name__ == "__main__":
    main()
