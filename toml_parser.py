import re
class TOMLParser:
    def __init__(s): s.data = {}
    def parse(s, text):
        current = s.data
        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"): continue
            # Table header
            m = re.match(r"^\[([^\]]+)\]$", line)
            if m:
                keys = m.group(1).split(".")
                current = s.data
                for k in keys: current = current.setdefault(k, {})
                continue
            # Key-value
            m = re.match(r'^([\w.]+)\s*=\s*(.+)$', line)
            if m:
                key, val = m.group(1).strip(), m.group(2).strip()
                current[key] = s._parse_value(val)
        return s.data
    def _parse_value(s, val):
        if val.startswith('"') and val.endswith('"'): return val[1:-1]
        if val.startswith("'") and val.endswith("'"): return val[1:-1]
        if val.lower() == "true": return True
        if val.lower() == "false": return False
        if val.startswith("["): return s._parse_array(val)
        try: return int(val)
        except:
            try: return float(val)
            except: return val
    def _parse_array(s, val):
        inner = val[1:-1].strip()
        if not inner: return []
        items = [s._parse_value(i.strip()) for i in inner.split(",") if i.strip()]
        return items
def demo():
    toml = """
[server]
host = "localhost"
port = 8080
debug = true

[database]
name = "myapp"
pool_size = 5
engines = ["postgres", "redis"]

[logging]
level = "info"
file = "/var/log/app.log"
"""
    p = TOMLParser(); data = p.parse(toml)
    print(f"Server: {data['server']}")
    print(f"DB engines: {data['database']['engines']}")
    print(f"Log level: {data['logging']['level']}")
if __name__ == "__main__": demo()\n