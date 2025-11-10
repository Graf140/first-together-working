import json
from apps.gps_tracking_service.config.redis import get_redis
from apps.gps_tracking_service.config.postgres import get_postgres_conn
from apps.shared.schemas.gps_tracking_service import GpsPoint

redis_client = get_redis()


async def start_track(user_id: str):
    # Инициализируем пустой трек в Redis
    await redis_client.delete(f"track:{user_id}")  # на случай дубля
    await redis_client.expire(f"track:{user_id}", 3600)  # TTL = 1 час


async def add_point(user_id: str, point: GpsPoint):
    await redis_client.lpush(f"track:{user_id}", point.model_dump_json())
    await redis_client.expire(f"track:{user_id}", 3600)


async def finish_track(user_id: str):
    # Получаем все точки из Redis
    points_raw = await redis_client.lrange(f"track:{user_id}", 0, -1)
    points = [GpsPoint.model_validate_json(p) for p in reversed(points_raw)]  # lpush → обратный порядок

    # Сохраняем в PostgreSQL
    conn = get_postgres_conn()
    try:
        cur = conn.cursor()
        # Создаём запись трека
        cur.execute("""
            INSERT INTO tracks (user_id, start_time, end_time, point_count)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (user_id, points[0].timestamp, points[-1].timestamp, len(points)))
        track_id = cur.fetchone()["id"]

        # Сохраняем точки
        for point in points:
            cur.execute("""
                INSERT INTO track_points (track_id, lat, lng, timestamp, altitude, speed)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (track_id, point.lat, point.lng, point.timestamp, point.altitude, point.speed))

        conn.commit()
        return track_id
    finally:
        cur.close()
        conn.close()
        await redis_client.delete(f"track:{user_id}")  # удаляем из Redis