# Scopes of permissions:

```
1: Login
2: View Dashboard
3: ... 
4: ...

```
Representation in binary. For every allowed scope a 1 is placed

**Example**:
If the user ist allowed to log in and to see the dashboard:
11 (bin) = 3 (dec)

To check if the user is only allowed to see the dashboard:

```
User scope:     11
Required scope: 01
AND             -- 
                01
```

If the required scope = the scope of the AND operator, the access is granted.