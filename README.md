# 📚 Library Management System

The **Library Management System** is a web application built using the Django framework, following the **Model-View-Template (MVT)** architectural pattern. This system helps to manage library resources efficiently, including books, authors, genres, and user borrowing records.

## 🚀 Features

- 📖 **Book Management**: Add, edit, delete, and view books in the library's collection.
- 🧑‍🤝‍🧑 **User Management**: Register, login, and manage user accounts.
- 🔄 **Book Borrowing**: Track book borrowing and return dates for users.
- 📝 **Author and Genre Management**: Add and manage authors and genres.
- 🔍 **Search**: Search functionality for books, authors, and genres.
- 📊 **Admin Panel**: Admin interface for managing books, users, authors, and other system entities.
- 🛡️ **User Roles**: Different roles (admin, librarian, member) with access control.
- 📨 **Notifications**: Email notifications for overdue books.

## 🛠️ Technologies Used

- **Django**: Backend web framework.
- **SQLite**: Default database used by Django.
- **HTML/CSS/JavaScript**: Frontend for the web pages.
- **Bootstrap**: Frontend framework for responsive design.
- **Django Admin**: Built-in admin panel for managing resources.

## 🏗️ MVT Structure

- **Model**: Defines the structure of the data (e.g., `Book`, `Author`, `Genre`, `User`, `Borrow`).
- **View**: Handles the request/response cycle, querying models and rendering templates.
- **Template**: Defines how the data is presented to the user using HTML templates.

## 🗃️ Database Schema

- **Book**: `title`, `author`, `genre`, `publish_date`, `isbn`, `availability`.
- **Author**: `first_name`, `last_name`, `date_of_birth`.
- **Genre**: `name`.
- **User**: `username`, `email`, `password`.
- **Borrow**: `user`, `book`, `borrow_date`, `return_date`.

## ⚙️ Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/library-management-system.git
