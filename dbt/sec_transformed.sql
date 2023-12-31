SELECT tickers,
        category,
        entitytype,
        exchanges,
        filingcount,
        cik,
        name,
        stateofincorporation,
        latestrevenuefilingdate,
        latestrevenueq10value,
        latestassestsfilingdate,
        latestassestsq10value,
        created_utc::date as utc_date,
        created_utc::time as utc_time
FROM dev.public.sec_table
