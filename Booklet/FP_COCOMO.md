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

| External Input            |               FTR | DET | Complexity (per IFPUG table) | Weight |
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

**Total UFP = ILF (36) + EIF (0) + EI (64) + EO (0) + EQ (33) = 97**\
Assuming the VAF to be 1.00, $\Rightarrow$ **AFP = UFP × VAF = 97 × 1.00 = 97 FP**

## LOC
Coefficient LOC/FP for the technologies used: 

let's assume two third of the code is frontend: 
React+TypeScript: 30–40 LOC/FP (UI + API calls). 

One third of the code is Backened:
Node/Express (TS): 30-45 LOC/FP (routing, service, validation).

FE 58 FP × 30 = 1.7k\
BE 28 FP × 30 ≈ 0.8k\
**Total ≈ 2.5KLOC**

# COCOCMO II

## COCOMO II Results (Post-Architecture Model)

- **Size estimate:** ~2.5 KLOC   
- **Constants:**  
  - A = 2.94  
  - B = 0.91  
  - C = 3.67  
  - D = 0.28  

- **Scale Factors (ΣSF):** ≈ 17.7  
- **Exponent (E):** 0.91 + 0.01 × 17.7 ≈ **1.087**  
- **Effort Multipliers (ΠEM):** ≈ 1.0 (nominal case)  

### Effort (Person-Months)
$PM = A \times Size^E \times \prod EM$  
$PM = 2.94 \times 2.5^{1.087} \times 1.0 ≈ 5 \, \text{PM}$

**Estimated effort:** ~5 person-months  

---

### Schedule (Time to Develop)
$TDEV = C \times PM^F$ 
where  
$F = D + 0.2 \times (E - B) = 0.28 + 0.2 \times (1.087 - 0.91) ≈ 0.315$
$TDEV = 3.67 \times 5^{0.315} ≈ 5.5 \, \text{months}$

**Estimated schedule:** ~5 months  

---

## Actual Outcome

Despite COCOMO II predicting **4 PM** and a **5-month schedule**, we successfully delivered the project in **4 months** with a **5-person team**.

### How we achieved this:
1. **Full parallelization** of tasks across frontend, backend, and DB.  
2. **Resource optimization**   
3. **Strict scope control** to prevent feature creep and keep the workload stable.  
4. **Efficient collaboration** with clear responsibilities and agile sprints.  