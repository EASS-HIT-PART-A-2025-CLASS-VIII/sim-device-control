import uvicorn

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sim_device_control.app:app", host="127.0.0.1", port=8000, reload=True)