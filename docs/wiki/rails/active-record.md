---
title: Active Record patterns
---

# Active Record patterns

Production Rails usually needs discipline:

- **N+1:** eager load with `includes` / `preload`; monitor with Bullet in dev.  
- **Transactions:** wrap multi-row updates; avoid long-held transactions open during I/O.  
- **Scopes:** composable named scopes beat giant query objects for readability.  
- **Migrations:** reversible where possible; index additions in separate deploy steps at scale.

These map loosely to Astra's **transactional task transitions** and **Postgres as source of truth** — same database rigour, different runtime shape.
