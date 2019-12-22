# `create_user_hook`

```python
create_user_hook.call_action(
    action: CreateUserAction,
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_deactivated: bool = False,
    is_moderator: bool = False,
    is_admin: bool = False,
    joined_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None
)
```

A filter for the function used to create new user account in the database.

Returns `User` dataclass with newly created user data.


## Required arguments

### `action`

```python
async def create_user(
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_deactivated: bool = False,
    is_moderator: bool = False,
    is_admin: bool = False,
    joined_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None
) -> User:
    ...
```

Next filter or built-in function used to create new user account in the database.


### `name`

```python
str
```

User name.


### `email`

```python
str
```

User e-mail address.


## Optional arguments

### `password`

```python
Optional[str] = None
```

User password. If not set, user will not be able to log-in to their account using default method.


### `is_moderator`

```python
bool = False
```

Controls if user can moderate site.


### `is_admin`

```python
bool = False
```

Controls if user user can administrate the site.


### `joined_at`

```python
Optional[datetime] = datetime.utcnow()
```

Joined at date for this user-account. Defaults to current date-time.


### `extra`

```python
Optional[Dict[str, Any]] = dict()
```

JSON-serializable dict with extra data for this user. This value is not used by Misago, but allows plugin authors to store additional information about user directly on their database row.