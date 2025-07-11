# tests/test_main.py 

from Dashboard.dashboard_model import load_data 
def test_load_data(): 
    df = load_data()
    print(f"DataFrame shape: {df.shape}")  # Debugging information 
    assert not df.empty, "DataFrame should not be empty"