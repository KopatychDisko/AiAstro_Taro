from .model import SessionLocal, UserBirthInfo, Message

def add_user(user_id, birth_date, birth_time=None, city=None, country=None, language=None):
    try:
        session = SessionLocal()
        user = UserBirthInfo(
            user_id=user_id,
            birth_date=birth_date,
            birth_time=birth_time,
            city=city,
            country=country,
            language=language
        )
        session.add(user)
        session.commit()
        session.refresh(user)  # Обновляем объект после коммита
        return user
    except Exception as e:
        session.rollback()
        print(f"Error adding user: {e}")
        raise
    finally:
        session.close()

# Получение пользователя по user_id
def get_user(user_id):
    try:
        session = SessionLocal()
        user = session.query(UserBirthInfo).filter(UserBirthInfo.user_id == user_id).first()
        if user:
            # Создаем копию данных, чтобы избежать проблем с сессией
            user_data = {
                'user_id': user.user_id,
                'birth_date': user.birth_date,
                'birth_time': user.birth_time,
                'city': user.city,
                'country': user.country,
                'language': user.language
            }
            return type('UserInfo', (), user_data)()  # Создаем объект с атрибутами
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        session.close()

# Добавление сообщения
def add_message(user_id, sender, text=None, html=None):
    try:
        session = SessionLocal()
        msg = Message(
            user_id=user_id,
            sender=sender,
            text=text,
            html=html
        )
        session.add(msg)
        session.commit()
        session.refresh(msg)  # Обновляем объект после коммита
        return msg
    except Exception as e:
        session.rollback()
        print(f"Error adding message: {e}")
        raise
    finally:
        session.close()

# Получение последних N сообщений
def get_last_messages(user_id, limit=10):
    try:
        session = SessionLocal()
        msgs = (
            session.query(Message)
            .filter(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )
        # Создаем копии данных, чтобы избежать проблем с сессией
        messages_data = []
        for msg in msgs:
            msg_data = {
                'role': msg.sender,
                'content': msg.text,
            }
            messages_data.append(msg_data)  # Создаем объект с атрибутами
        return list(reversed(messages_data))
    except Exception as e:
        print(f"Error getting messages: {e}")
        return []
    finally:
        session.close()

def update_user(user_id: str, birth_date = None, birth_time = None, city: str = None, country: str = None, language=None):
    try:
        with SessionLocal() as session:
            user = session.query(UserBirthInfo).filter_by(user_id=user_id).first()
            if not user:
                # Если пользователя нет, создаем нового
                user = UserBirthInfo(
                    user_id=user_id,
                    birth_date=birth_date or "",
                    birth_time=birth_time,
                    city=city,
                    country=country,
                    language=language
                )
                session.add(user)
            else:
                # Обновляем существующего пользователя
                if birth_date:
                    user.birth_date = birth_date
                if birth_time:
                    user.birth_time = birth_time
                if city:
                    user.city = city
                if country:
                    user.country = country
                if language:
                    user.language = language
            session.commit()
            session.refresh(user)  # Обновляем объект после коммита
            return user
    except Exception as e:
        print(f"Error updating user: {e}")
        raise

def get_all_users():
    session = SessionLocal()
    try:
        users = session.query(UserBirthInfo).all()
        print("📋 All users in DB:")
        for u in users:
            print(f"""
👤 UserID: {u.user_id}
   🌍 Birth place: {u.city}, {u.country}
   🎂 Date: {u.birth_date}
   ⏰ Time: {u.birth_time}
""")
        return users
    finally:
        session.close()


# --- Тест ---
if __name__ == "__main__":
    # Добавим пользователя
    add_user(
        user_id="109935806661774952481",
        birth_date="30.08.1999",   # str
        birth_time="12:45",        # str
        city="Moscow",
        country="Russia"
    )

    # Получим всех пользователей
    get_all_users()
