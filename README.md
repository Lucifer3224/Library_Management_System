# 📚 Magical Library Management System 🪄

Welcome to the enchanted world of book management! 🧙‍♂️✨

## 🌟 Features That'll Make You Say "Wow!"

- 🔐 Secure User Authentication (Login/Register)
- 🔍 Mystical Book Discovery and Search
- 🎧 Spellbinding Audio Book Support
- 📚 Personal Library (Like Your Own Miniature Hogwarts Library!)
- 👤 User Profile Management (Be the Protagonist of Your Own Story)
- 📑 Category-based Book Browsing (Adventure? Mystery? Romance? We've Got It All!)

## 🧙‍♂️ Installation Magic

1. Summon the repository:
   ```
   git clone https://github.com/yourusername/library-management-system.git
   ```

2. Enter the magical realm:
   ```
   cd library-management-system
   ```

3. Cast the spell to install dependencies:
   ```
   pip install -r requirements.txt
   ```

## 🧪 Usage Potion

Mix the following ingredients in your cauldron (or just run this command):

```
python library_app.py
```

## 📜 Scroll of File Structure

- 📘 `library_app.py`: The main spellbook
- 📂 `models/`: Chambers of functionality
  - 🔑 `login_frame.py`: The key to enter
  - 📝 `register_frame.py`: New wizard registration
  - 📚 `library_frame.py`: The grand library hall
- 📂 `instance/`: Secret chambers
  - ⚙️ `config.py`: Magical configurations
  - 🧙‍♂️ `admin_credentials.py`: Dumbledore's login
- 📂 `static/`: Treasury of images and icons
- 📂 `Data/`: The restricted section
  - 📚 `Books/`: Tomes of knowledge
  - 🎧 `Audio/`: Enchanted audiobooks
  - 🖼️ `Covers/`: Mystical book covers
  - 📑 `Categories/`: Scrolls of categorization

## 🗃️ Magical Database Schema

Our mystical MySQL database, `library_management_system`, contains these enchanted tables:

### 📚 Books Table
- `book_id` 🔑
- `title` 📖
- `author` ✍️
- `genre` 🏷️
- `isbn` 🔢
- `publication_year` 📅
- `lang` 🌐
- `pages` 📄
- `date_added` 🗓️
- `summary` 📜

### 👥 Readers Table
- `id` 🔑
- `first_name` 📛
- `last_name` 📛
- `email` 📧
- `user_name` 👤
- `pass` 🔐
- `age` 🎂

### 📖 Readers_Books Table
- `user_name` 👤
- `isbn` 📘

This magical schema allows our library to keep track of all books, readers, and which books each reader has borrowed!

## 🧪 Magical Dependencies

- 🖌️ customtkinter (For that sleek, modern look)
- 🖼️ PIL (Picture-perfect imaging)
- 🐬 mysql-connector-python (Connects to the mystical database)
- 🎵 pygame (For audio book enchantments)
- 📂 os (Navigate the file system like a magical map)
- 🎧 aifc (Handle audio files with the precision of a sound wizard)

## 📜 Scroll of License

This project is protected by the [MIT License](LICENSE) spell.

## 🙏 Acknowledgements

You can reach me at [habibamowafy24@gmail.com](mailto:habibamowafy24@gmail.com). 🧙‍♀️✨
