# Patient Management System

This project combines a FastAPI backend with a Streamlit frontend for managing patient records stored in `patients.json`.

## What It Does

- View all patients
- Fetch a patient by ID
- Sort patients by `bmi`, `height`, or `weight`
- Create a new patient
- Update an existing patient
- Delete a patient
- Use a Streamlit UI to interact with the API

## What It Can Be Used For

- Learning FastAPI CRUD operations with a simple real-world example
- Practicing Pydantic models, field validation, and computed fields
- Building a small healthcare-style dashboard with Streamlit
- Managing sample patient records without setting up a database
- Demonstrating how a Python frontend can interact with a REST API

## Project Files

- `main.py`: FastAPI application with patient CRUD and sorting endpoints
- `app.py`: Streamlit frontend for viewing and managing patients
- `patients.json`: Local data store used by the API

## Tech Stack

- FastAPI
- Pydantic
- Streamlit
- Pandas
- Requests

## Run Locally

1. Create and activate a virtual environment.
2. Install the required packages:

```bash
pip install fastapi uvicorn streamlit pandas requests pydantic
```

3. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

4. In a new terminal, start the Streamlit app:

```bash
streamlit run app.py
```

5. Open the Streamlit URL shown in the terminal, usually `http://localhost:8501`.

The frontend expects the FastAPI backend to be running at `http://127.0.0.1:8000`.

## How It Works

1. The FastAPI app in `main.py` starts a local API server.
2. Patient records are read from and written to `patients.json`.
3. When a new patient is created or an existing one is updated, Pydantic validates the input data.
4. The `Patient` model computes `bmi` and a health `verdict` automatically from the patient's height and weight.
5. The Streamlit app in `app.py` sends HTTP requests to the FastAPI endpoints.
6. Users can view, add, edit, delete, and sort patient records from the Streamlit interface.

In short, `main.py` handles the business logic and data validation, while `app.py` provides a simple UI on top of those API routes.

## API Endpoints

### `GET /`

Returns a welcome message for the API.

### `GET /view`

Returns all patient records from `patients.json`.

### `GET /patient/{patient_id}`

Returns a single patient by ID.

Example:

```bash
curl http://127.0.0.1:8000/patient/P001
```

### `GET /sort?sort_by=bmi&order=asc`

Sorts patients by one of:

- `bmi`
- `height`
- `weight`

The `order` query parameter accepts `asc` or `desc`.

### `POST /create`

Creates a new patient and automatically computes:

- `bmi`
- `verdict`

Example request body:

```json
{
  "id": "P013",
  "name": "Rahul Sen",
  "city": "Kolkata",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 72.0
}
```

### `PUT /edit/{patient_id}`

Updates an existing patient. Any provided fields are validated again through the Pydantic model before saving.

### `DELETE /delete/{patient_id}`

Deletes a patient record by ID.

## Data Model

Each patient includes:

- `id`
- `name`
- `city`
- `age`
- `gender`
- `height`
- `weight`
- `bmi`
- `verdict`

`bmi` is computed from `weight / height^2`, and `verdict` is derived from BMI:

- Below `18.5`: `Underweight`
- Below `25`: `Normal`
- Below `30`: `Overweight`
- `30` and above: `Obese`

## Streamlit UI

The Streamlit app in `app.py` provides four sections:

- `View Patients`
- `Add Patient`
- `Edit Patient`
- `Delete Patient`

It communicates with the FastAPI backend using HTTP requests.

## Notes

- Patient data is stored locally in `patients.json`.
- The Streamlit app assumes the backend is already running.
- No database is used in this version of the project.
