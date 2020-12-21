from fastapi import FastAPI, HTTPException
import redis, secrets, string, json
import default

app = FastAPI()

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

ROOM_CHARS = string.ascii_uppercase

def validuname(uname: str):
    if uname == "":
        return False

@app.get("/")
async def root():
    return {"message": "hello"}

@app.get("/create")
async def create():
    room_id = ''.join(secrets.choice(ROOM_CHARS) for i in range(4))
    while r.sismember("rooms", room_id):
        room_id = ''.join(secrets.choice(ROOM_CHARS) for i in range(4))
    pipe = r.pipeline()
    pipe.sadd("rooms", room_id)
    room_hash = "room:" + room_id
    pipe.hset(room_hash, "users", "[]")
    pipe.hset(room_hash, "texts1", default.texts1())
    pipe.hset(room_hash, "texts2", default.texts2())
    pipe.hset(room_hash, "texts3", default.texts3())
    pipe.hset(room_hash, "images", default.images())
    pipe.execute()

@app.get("/join")
async def join(room: str, uname: str):
    if not validuname(uname):
        raise HTTPException(status_code=400,
                detail="uname contains forbidden characters")
    if not r.sismember("rooms", room):
        raise HTTPException(status_code=404, detail="Room not found")

    room_hash = "room:" + room
    room_users = json.loads(r.hget(room_hash, "users"))
    room_users.append(uname)
    r.hset(room_hash, "users", json.dumps(room_users))

    return r.hgetall(room_hash)
