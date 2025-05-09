def swagger_template():
    return {
        "swagger": "2.0",
        "info": {
            "title": "Contact Notes API",
            "description": "A simple API to manage contacts and notes",
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/api",
        "schemes": ["http"],
        "paths": {}
    }

def swagger_contact_paths():
    return {
        "/contacts": {
            "post": {
                "summary": "Create a new contact",
                "description": "Adds a new contact to the database",
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "description": "Contact data",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "full_name": {"type": "string"},
                                "email": {"type": "string"},
                                "phone": {"type": "string"}
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Contact created"},
                    "400": {"description": "Invalid input"},
                    "401": {"description": "Unauthorized"}
                }
            },
            "get": {
                "summary": "Get all contacts",
                "description": "Returns a list of all contacts",
                "produces": ["application/json"],
                "responses": {
                    "200": {"description": "List of contacts"}
                }
            }
        },
        "/contacts/{id}": {
            "get": {
                "summary": "Get a specific contact",
                "description": "Returns a single contact by ID",
                "produces": ["application/json"],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "Contact ID"
                    }
                ],
                "responses": {
                    "200": {"description": "Contact found"},
                    "404": {"description": "Contact not found"}
                }
            },
            "put": {
                "summary": "Update a contact",
                "description": "Updates the details of an existing contact",
                "consumes": ["application/json"],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "Contact ID"
                    },
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "full_name": {"type": "string"},
                                "email": {"type": "string"},
                                "phone": {"type": "string"}
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {"description": "Contact updated"},
                    "404": {"description": "Contact not found"}
                }
            },
            "delete": {
                "summary": "Delete a contact",
                "description": "Removes a contact from the database",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "Contact ID"
                    }
                ],
                "responses": {
                    "200": {"description": "Contact deleted"},
                    "404": {"description": "Contact not found"}
                }
            }
        }
    }
