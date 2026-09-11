1. Open ChromaDB.

2. Load my local embedding model.

3. Create a knowledge-base collection.

4. Add my documents.

5. Convert those documents into vectors.

6. Store those vectors in ChromaDB.

7. User asks:
   "How do I stop being charged?"

8. Convert the question into a vector.

9. Compare the question vector
   with all stored document vectors.

10. Find the closest documents.

11. Return the top 2.

12. Print them


### Why `PersistentClient`?

Because you want the data to remain after your Python program stops.

Without persistence:

```
Run program
   ↓
Store data
   ↓
Stop program
   ↓
Data may disappear
```

With persistence:

```
Run program
   ↓
Store data
   ↓
Stop program
   ↓
Data remains on disk ✅
```

Your code is basically saying.
