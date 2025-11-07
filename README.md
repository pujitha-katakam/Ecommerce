# Ecommerce
Snazzy – E-commerce Platform for Jewellery :Developed a Django-based web app enabling users to browse and purchase cultural jewelry styles. Integrated backend logic, user feedback, and SQL database operations.

## Deploying on Render

1. Push your latest changes (including `render.yaml`) to GitHub.
2. Create a new Web Service on Render and connect it to your repository.
3. Render detects `render.yaml` and provisions a Python web service named `snazzy-ecommerce`.
4. Set the following environment variables in Render:
   - `SECRET_KEY`: a secure random string.
   - `DEBUG`: `False` for production.
   - `ALLOWED_HOSTS`: optional if you need additional hosts (defaults already include Render).
   - `DATABASE_URL`: provided automatically when you add a Render PostgreSQL database (required for production persistence).
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and other mail credentials if you plan to send emails.
   - `STRIPE_SECRET_KEY` and related keys when enabling Stripe payments.
5. If you need persistent user-uploaded media, keep the managed disk created in `render.yaml` (1 GB by default). Increase the size from the Render dashboard if you expect more uploads.
6. Render will run `pip install -r requirements.txt` and `python manage.py collectstatic --noinput` during the build, run database migrations after deployment, and start the app with `gunicorn ec.wsgi:application`.
7. After the service is live, visit the Render URL to confirm the site loads and create an admin user with `python manage.py createsuperuser` through a Render shell if needed.