<!-- troubleshooting.md -->
# Troubleshooting Guide

## Common Issues

### MongoDB Connection Issues

**Problem**: Unable to connect to MongoDB
```
Solution: 
- Verify MongoDB is running: `mongod --version`
- Check connection string in config
- Ensure correct port (default: 27017)
```

### Test Database Conflicts

**Problem**: Tests failing due to dirty database state
```
Solution:
- Use mock_db fixture for isolation
- Clear test database before runs
- Use function-scoped fixtures
```

### Authentication Issues

**Problem**: Tests failing with unauthorized access
```
Solution:
- Verify authenticated_client fixture
- Check session management
- Ensure proper test user setup
```

## Debug Tips

1. Enable Flask debug mode
2. Use pytest's `-v` flag for verbose output
3. Check application logs
4. Verify environment variables

---