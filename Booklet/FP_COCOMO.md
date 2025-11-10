# Function Point analysis
## ILF
| ILF                     | DET | RET  | Complexity                          | Weight |
| ----------------------- | -----------------------: | -------------------: | ----------------------------------- | -----: |
| User               |                       6 |                    2 | Low  |     6 |
| Monster              |                       6 |                    1 | Low                        |     6 |
| Item           |                       6 |                    1 | Low                         |     6 |
| Encounter          |                        2 |                    1 | Low                         |     6 |
| Inventory     |                        2 |                    1 | Low                             |      6 |
| Collection |                        2 |                    1 | Low                             |      6 |
| **Total ILF = 36 FP**   |                          |                      |                                     |        |
## EIF

| EIF                              | DET | RET | Complexity  | Weight |
| -------------------------------- | --: | --: | ----------- | -----: |
| **Total EIF = 0 FP**            |     |     |             |        |

## EI

| EI            |               FTR | DET | Complexity | Weight |
| ------------------------- | ----------------------------------------: | --: | ---------------------------- | -----: |
| Registration              |                          2  |   6 | Medium    |      4 |
| Login                     |                                  1  |   2 | Low                      |      3 |
| Update User            |                                         1 |   5 | Low                      |      3 |
| Delete User              |                        2 |   1 | Low                      |      3 |
| Create Monster              | 2 |   5 | Medium                      |      4 |
| Update Monster           |                    2 |   6 | Medium                      |      4 |
| Delete Monster              |                        2 |   1 | Low                      |      3 |
| Create Item              | 2 |   5 | Medium                      |      4 |
| Update Item           |                    2 |   6 | Medium                      |      4 |
| Delete Item              |                        2 |   1 | Low                      |      3 |
| Create Encounter                      |                     6 |   6 | High                      |      6 |
| Delete Encounter                      |                     1 |   1 | Low                      |      3 |
| Catch Monster                      |                     6 |   11 | High                      |      6 |
| Buy Item                      |                     3 |   9 | Medium                      |      4 |
| Shard Monster                      |                     2 |   4 | Low                      |      3 |
| Complete Collection                      |                     3 |   6 | Medium                      |      4 |
| Start Timer                      |                     1 |   2 | Low                      |      3 |
| **Total EI = 64 FP**      |                                           |     |                              |        |
## EO
| EO                             | FTR | DET | Complexity            | Weight |
| ------------------------------ | --: | --: | --------------------- | -----: |
| **Total EO = 0 FP**           |     |     |                       |        |

## EQ
| EQ                    | FTR | DET | Complexity | Weight |
| --------------------- | --: | --: | ---------- | -----: |
| Get User by id      |   1 |   4 | Low        |      3 |
| Get all Users      |   1 |   4 | Low    |      3 |
| Get Monster by id     |   1 |   6 | Low    |      3 |
| Get all Monsters |   1 |   6 | Low    |      3 |
| Get Item by id |   1 |   6 | Low    |      3 |
| Get all Items |   1 |   6 | Low    |      3 |
| Get Encounter by id |   1 |   5 | Low    |      3 |
| Get all Encounters |   1 |   5 | Low    |      3 |
| Get Collection by player |   1 |   3 | Low    |      3 |
| Get Items by player |   1 |   3 | Low    |      3 |
| Get Statistics |   1 |   3 | Low    |      3 |
| **Total EQ = 33 FP**  |     |     |            |        |

**Total UFP = ILF (36) + EIF (0) + EI (64) + EO (0) + EQ (33) = 97**

Considering the 14 GSCs being rated as below:

| GSC                    | Rating | 
| --------------------- | --: | 
| Data communication      |   4 | 
| Distributed data processing      |   4 | 
| Performance     |   3 |  
| Heavily used configuration |   2 | 
| Transaction rate |   3 | 
| On-line data entry |   4 | 
| End-user efficiency |   4 | 
| On-line update |   4 | 
| Complex processing |   3 | 
| Reusability |   3 | 
| Installation ease |   3 | 
| Operational ease |   4 | 
| Multiple sites |   2 | 
| Facilitate change |   3 | 
| **Total = 46**  |     | 

Computing the **VAF = 0.65 + (0.01 * ΣGSC) = 0.65 + (0.01 * 46) = 1.11**, we get the Adjusted Function points as **AFP = UFP × VAF = 97 × 1.11 = 107.67 FP**

## LOC

Let's assume two thirds of the code is frontend: 
Vue + JavaScript: 45–50 LOC/FP (UI + API calls). 

One third of the code is backend:
Python: 42 LOC/FP (routing, service, validation).

FE 71.78 FP × 45 = 3.2k\
BE 35.89 FP × 42 ≈ 1.5k\
**Total ≈ 4.7 KLOC**

# COCOMO II

## COCOMO II Results (Post-Architecture Model)

- **Size estimate:** ~4.7 KLOC   
- **Constants:**  
  - A = 2.94  
  - B = 0.91  
  - C = 3.67  
  - D = 0.28  

Using the official COCOMO II calibration table, we compute the 5 scale factors:

| Scale Factor                    | Rating | 
| --------------------- | --: | 
| PREC     |   2.48 (High) | 
| FLEX     |   1.01 (Very high) | 
| RESL     |   5.07 (Nominal) |  
| TEAM     |   1.10 (Very High) | 
| PMAT     |   4.68 (Nominal) | 

- **Scale Factors (ΣSF):** ≈ 14.34  
- **Exponent (E):** 0.91 + 0.01 × 14.34 ≈ **1.053**  
- **Effort Multipliers (ΠEM):** ≈ 1.0 (nominal case)  

### Effort (Person-Months)
$PM = A \times Size^E \times \prod EM$  
$PM = 2.94 \times 4.7^{1.053} \times 1.0 ≈ 14.9 \ \text{PM}$

**Estimated effort:** ~15 person-month

---

### Schedule (Time to Develop)
$TDEV = C \times PM^F$ 
where
$F = D + 0.2 \times (E - B) = 0.28 + 0.2 \times (1.053 - 0.91) ≈ 0.308$
$TDEV = 3.67 \times 15^{0.308} ≈ 8.45 \ \text{months}$

**Estimated schedule:** ~8 months  

---

## Actual Outcome

Despite COCOMO II predicting **15 PM** and a **8-month schedule** (meaning a staffing of ~2 people), we successfully delivered the project in **2 months** with a **3-person team**.

### How we achieved this:
1. **Full parallelization** of tasks across frontend, backend, and DB.  
2. **Resource optimization**   
3. **Strict scope control** to prevent feature creep and keep the workload stable.  
4. **Efficient collaboration** with clear responsibilities and agile sprints.
