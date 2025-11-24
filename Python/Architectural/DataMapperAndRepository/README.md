# Data Mapper and Repository Pattern
This project is an educational and simplified implementation of two important database-related patterns: **Data Mapper** and **Repository**.  
The focus of this project is on **explaining the differences, layers, the role of each pattern, and the place of technical and business logic**.

---

## Project Structure (Four Layers)
The project has four layers, organized from the lowest (closest to the database) to the highest (closest to the consumer):

### 1. `UserDomainObject`
- A pure **domain object**.  
- No interaction with the database or queries.  
- Only stores data structure and basic rules.  
- Fully independent of other layers.

### 2. `UserDataMapper`
- Responsible for **mapping between domain objects and the database**.  
- Only generates queries and converts results to Domain Objects.  
- No business logic or decision-making at this level.  
- Example operations:  
  - Save  
  - Retrieve  
  - Delete  

### 3. `UserRepository`
- One level above DataMapper.  
- Provides a **high-level interface** for working with data.  
- Uses DataMapper but has broader responsibilities:  
  - Higher-level technical logic  
  - Combining multiple Mapper operations  
  - Basic validation  
- This is where **technical logic** is implemented, not business logic.  
- Example operations:  
  - Check existence before saving  
  - Check existence before deleting  
  - Execute multiple queries together  

### 4. `Client.py`
- Example of system usage.  
- Uses all the above layers (Domain, Mapper, Repository).  
- Only acts as a caller; no specific logic is implemented here.

---

## Pattern Goals

### Data Mapper Pattern
- A **Data Access** pattern.  
- Goal: complete separation of Domain Objects from the database.  
- Queries are built only at this level.  
- Domain Object has no knowledge of the Mapper.

### Repository Pattern
- An **Architectural / Domain-Oriented** pattern.  
- Goal: place a high-level layer between Business Logic and Data Access.  
- Views / Services / Controllers call Repository methods instead of writing queries.  
- Repository acts as the link between Business Logic and Mapper.

---

## Key Differences

### Roles
- **Data Mapper:** translates data ↔ database  
- **Repository:** manages collections of objects + high-level operational logic  

### Logic
- **Logic in Mapper:**  
  - No business logic  
  - Only queries and persistence  
- **Logic in Repository:**  
  - Technical logic  
  - Basic validation  
  - Combining Mapper operations  

### Domain interaction
- **Mapper:** fully dependent on the database  
- **Repository:** a higher layer that uses the Mapper  
- **Domain Object:** fully independent of both database and Repository  

### Architectural placement
- **Data Mapper:** part of Data Access layer  
- **Repository:** part of Architectural / Domain Access layer  

---

## Place of Technical and Business Logic

### Technical Logic
Where it should be implemented:  
- Repository  

Where it should NOT be implemented:  
- DataMapper  
- DomainObject  

### Business Logic
Not included in this project,  
but in a real project it should reside in:  
- **Service Layer**  
- **Domain Service**  

Repository only provides prerequisites for business logic, not its implementation.
