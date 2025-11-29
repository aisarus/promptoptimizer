# 🔄 DEV vs PRODUCTION Versions

## Port Differences

### DEV VERSION (This folder)
- **Backend API:** http://localhost:8001
- **Frontend UI:** http://localhost:8081
- **Swagger UI:** http://localhost:8001/docs

### PRODUCTION VERSION (Original folder)
- **Backend API:** http://localhost:8000
- **Frontend UI:** http://localhost:8080
- **Swagger UI:** http://localhost:8000/docs

## Why Different Ports?

This allows you to run **BOTH versions simultaneously**:
- Production version keeps working (8000/8080)
- Dev version for experiments (8001/8081)

## Files Modified for DEV

1. `backend/app/config.py` - PORT changed to 8001
2. `frontend/static/js/api-client.js` - API_BASE_URL uses port 8001
3. `start_backend.bat` - Launches on port 8001
4. `start_frontend.bat` - Launches on port 8081
5. `start_all.bat` - Uses both new ports

## Safe Development Workflow

```
1. Make changes in DEV version (this folder)
2. Test on ports 8001/8081
3. If it works → copy files to PRODUCTION version
4. If it breaks → delete DEV folder and start fresh from backup
```

## Quick Commands

### Run DEV version:
```bash
start_all.bat
```

### Run PRODUCTION version:
```bash
cd ../prompt-optimizer-saas
start_all.bat
```

### Run BOTH at same time:
1. Start PRODUCTION (8000/8080)
2. Start DEV (8001/8081)
3. Compare results side-by-side!

## Backup Strategy

Always keep:
- `prompt-optimizer-saas/` - Original working version ✅
- `prompt-optimizer-saas-dev/` - Current experiments 🔧
- `prompt-optimizer-saas-backup/` - Emergency backup 🆘

If DEV breaks → Just delete and copy from original again!
