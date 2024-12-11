<!-- database.md -->
# Database Schema

## Collections

### Users Collection

```javascript
{
    "_id": ObjectId,
    "email": string,
    "password": string,  // Hashed password
    "tasks": [ObjectId]  // Array of task IDs
}
```

### Tasks Collection

```javascript
{
    "_id": ObjectId,
    "name": string,
    "priority": string,
    "user_id": ObjectId
}
```

## Indexes

### Users Collection
- Unique index on `email` field
- Index on `tasks` array

### Tasks Collection
- Index on `user_id` field
- Compound index on `name` and `user_id`

---