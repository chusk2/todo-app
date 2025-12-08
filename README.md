# 📋 Streamlit TODO List Manager

Welcome to your personal Streamlit-powered TODO List Manager! This application helps you efficiently manage your daily tasks with a simple and intuitive user interface. Built with Streamlit and SQLite, it provides a robust and easy-to-use solution for staying organized.

## ✨ Features

This application offers the following core functionalities:

-   **➕ Create Tasks**: Easily add new tasks to your list with a dedicated input form.
-   **📋 Read Tasks**: View all your tasks in a clear, sortable, and filterable table.
-   **🔄 Update Tasks**: Modify existing tasks directly within the table. You can edit descriptions, mark tasks as completed, and the changes are saved instantly.
-   **🗑️ Delete Tasks**: Select and remove tasks you no longer need from your list.
-   **Debug Mode**: A toggleable debug mode provides detailed insights into the application's internal workings, useful for development and troubleshooting.

## 🚀 Technologies Used

*   **Python**: The core programming language.
*   **Streamlit**: For building the interactive web application.
*   **SQLite**: A lightweight, file-based database for storing tasks.
*   **Pandas**: For efficient data manipulation and integration with Streamlit's data editor.

## 🛠️ Setup and Installation

Follow these steps to get the TODO List Manager up and running on your local machine.

### 1. Clone the Repository

First, clone this GitHub repository to your local machine:

```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
```

### 2. Create a Virtual Environment (Recommended)

It's good practice to use a virtual environment to manage project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

*(Note: You might need to create a `requirements.txt` file if it doesn't exist, by running `pip freeze > requirements.txt` after installing Streamlit and Pandas.)*

### 4. Run the Application

Once the dependencies are installed, you can launch the Streamlit application:

```bash
streamlit run Home.py
```

Your browser should automatically open to the application (usually at `http://localhost:8501`).

## 💡 Usage

Navigate through the different pages using the sidebar:

-   **Home**: Overview of the application.
-   **Create tasks**: Add new tasks.
-   **Read tasks**: View your current tasks.
-   **Update tasks**: Edit task descriptions or mark them as complete.
-   **Delete tasks**: Select and remove tasks.

You can toggle the **"Debug Mode"** on any page to see detailed operational messages, which can be helpful for understanding the app's flow or troubleshooting.

## 📂 Project Structure

```
todo-app/
├── Home.py                 # Main application entry point and homepage
├── db_path.py              # Defines the path to the SQLite database
├── debug.py                # Debugging utilities (add_debug_message, show_debug_messages)
├── pages/
│   ├── 1_➕_Create_task.py  # Page for adding new tasks
│   ├── 2_📋_Read_tasks.py   # Page for viewing all tasks
│   ├── 3_🔄_Update_tasks.py # Page for editing existing tasks
│   └── 4_🗑️_Delete_tasks.py # Page for deleting tasks
├── tasks.db                # SQLite database file (will be created automatically)
└── requirements.txt        # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## 📄 License

This project is open source and available under the MIT License.

## 📧 Contact

If you have any questions, suggestions, or just want to connect, feel free to reach out!

-   **GitHub**: [@chusk2](https://github.com/chusk2)
-   **Nickname**: danicoder