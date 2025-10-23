# Movie Recommendation System API

A Django REST API for managing movies, user reviews, watched movies, and personalized movie recommendations using a content-based machine learning approach.

---

## Features

* User registration, login, and profile management
* CRUD operations for movies (admin-only)
* Add, update, delete, and view reviews
* Mark movies as watched
* Search movies by title, description, or director
* Personalized movie recommendations using a content-based recommendation engine

---

## Tech Stack

* **Backend:** Django, Django REST Framework
* **Authentication:** JWT (SimpleJWT)
* **Database:** SQLite (default, can be changed)
* **ML:** Scikit-learn (`TfidfVectorizer` + `cosine_similarity`)

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone <repository-url>
cd <project-folder>
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser (admin)**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

7. **Access API**

* Admin panel: `http://localhost:8000/admin/`
* API root: `http://localhost:8000/api/`

---

## API Endpoints (examples)

| Endpoint                   | Method | Description                |
| -------------------------- | ------ | -------------------------- |
| `/api/user_register/`      | POST   | Register a new user        |
| `/api/login/`              | POST   | Login and get JWT tokens   |
| `/api/profile/`            | GET    | Get logged-in user profile |
| `/api/movies/`             | GET    | List all movies            |
| `/api/add_movie/`          | POST   | Add new movie (Admin only) |
| `/api/add_review/<id>/`    | POST   | Add review to a movie      |
| `/api/watchedmovies/`      | POST   | Mark movie as watched      |
| `/api/movies/recommended/` | GET    | Get recommended movies     |

---

## Machine Learning Approach

The project implements a **content-based recommendation system** using **TF-IDF vectorization** and **cosine similarity**:

1. **Feature Extraction**

   * Combines each movie's genres and description into a single text string.
   * TF-IDF vectorizer converts text into numerical feature vectors.

2. **Similarity Computation**

   * Computes cosine similarity between all movies.
   * Higher similarity scores indicate more similar content.

3. **User Preferences**

   * Considers movies the user rated highly (>= 4/5).
   * Recommends movies similar to those highly rated ones.
   * Weighted by user's rating to prioritize preferences.

4. **Fallback**

   * If a user has no reviews, returns **popular movies** based on average rating and review count.

---

## Notes

* Only admins can add/update/delete movies.
* Users can only edit or delete their own reviews.
* Watching a movie increments its `watched_count` via Django signals.

---

## Dependencies

* Django
* djangorestframework
* djangorestframework-simplejwt
* scikit-learn
* numpy

---

## License

MIT License
