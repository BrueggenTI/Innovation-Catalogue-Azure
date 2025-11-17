# Brüggen Innovation Catalogue

This is the web application for the Brüggen Innovation Catalogue.

## Deployment

When deploying a new version of the application that includes changes to the database models, you must run the database migration script to update the production database schema.

After deploying the new code, run the following command in the application's shell environment:

```bash
flask db upgrade
```

This command will apply any new database migrations and ensure the database schema is up to date with the application code. Failure to do so may result in application errors.
