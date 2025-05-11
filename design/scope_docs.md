# Scopes of permissions:

```
1: Login | 1
2: View Dashboard | 2
3: View Container | 4
4: Get Container | 8
5: See all Containers | 16
6: View Apps / Compose | 32
7: Create Apps / Compose | 64

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