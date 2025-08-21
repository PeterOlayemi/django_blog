# Django Blog

A modern, feature-rich blog platform built with Django.  
This project demonstrates best practices in Django development, clean UI/UX, and a robust set of features for both writers and readers.

---

## 🚀 Features

### 📝 Article Management
- **Create, Edit, Delete Articles:** Authenticated users can write, update, and remove their own posts.
- **Rich Text Content:** Articles support formatted text and images.
- **Categories & Tags:** Organize articles by categories and tags for easy navigation.
- **Article Images:** Upload and display cover images for each article.
- **Reading Time Estimate:** Automatic calculation and display of estimated reading time.

### 👥 User System
- **User Registration & Authentication:** Secure sign-up, login, and logout.
- **Profile Pages:** Each user has a customizable profile with avatar, bio, and stats.
- **Profile Picture Upload:** Users can upload and update their profile images.
- **Password Change:** Secure password change functionality.

### 💬 Comments & Replies
- **Threaded Comments:** Readers can comment on articles and reply to other comments.
- **Edit/Delete Own Comments:** Users can manage their own comments and replies.
- **Live Comment Count:** Real-time display of the number of comments per article.

### 👍 Likes & Engagement
- **Like/Unlike Articles:** Users can like or unlike articles, with like counts displayed.
- **Related Posts:** Suggests similar articles based on category or tags.

### 🔍 Search & Navigation
- **Full-Text Search:** Quickly find articles by title or content.
- **Category & Tag Browsing:** Filter articles by category or tag.
- **Pagination:** Clean navigation for browsing large numbers of posts.

### 📬 Newsletter & Social
- **Newsletter Signup:** Readers can subscribe to updates.
- **Social Sharing:** Share articles on popular social platforms.

### 🌗 Light/Dark Mode
- **Theme Toggle:** Switch between light and dark modes for comfortable reading.

### 🛡️ Security & Best Practices
- **CSRF Protection:** All forms are protected against CSRF attacks.
- **User Permissions:** Only authors can edit or delete their own content.
- **Input Validation:** All user input is validated and sanitized.

---

## 🏗️ Project Structure

```
django_blog/
├── account/         # User authentication, profiles
├── blog/            # Article models, views, templates
├── core/            # Core site features (homepage, about, etc.)
├── django_blog/     # Project folder (settings, main urls, etc.)
├── media/           # Uploaded images (articles, profiles)
├── static/          # Static files (CSS, JS, images)
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PeterOlayemi/django-blog.git
   cd django_blog
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY = your-django-secret-key
   email = your-email@example.com
   appsPassword = your-app-specific-password
   ```

   - `SECRET_KEY`: Your Django secret key (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
   - `email`: The email address used for sending emails (e.g., for password reset, newsletter)
   - `appsPassword`: The app-specific password for your email provider (e.g., Gmail App Password)

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the site:**
   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🧑‍💻 Development

- **Static files:** Place CSS, JS, and images in `static/`.
- **Media files:** Uploaded images are stored in `media/`.
- **Templates:** Use Django templating in `templates/` directories.

---

## 📝 Customization

- **Branding:** Update colors and logos in `static/css/base.css` and `static/images/`.
- **Email/Newsletter:** Configure email backend in `settings.py` for newsletter features.
- **Social Links:** Add your social media URLs in the footer template.

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Credits

- Built with [Django](https://www.djangoproject.com/)
- UI inspired by modern blog platforms
- Icons from [Font Awesome](https://fontawesome.com/)

---

## 📫 Contact

For questions or collaboration, reach out via [olayemipeter177@gmail.com](mailto:olayemipeter177@gmail.com) or open an issue.

---

**Star this repo** ⭐ if you like it, and feel free to fork for your own portfolio
