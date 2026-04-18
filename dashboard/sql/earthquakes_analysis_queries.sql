USE global_seismic_trends;
CREATE TABLE earthquakes (
    id VARCHAR(50) PRIMARY KEY,

    mag FLOAT,
    place TEXT,
    time DATETIME,
    updated DATETIME,
    tz FLOAT,

    url TEXT,
    detail TEXT,

    felt FLOAT,
    cdi FLOAT,
    mmi FLOAT,
    alert VARCHAR(20),

    status VARCHAR(20),
    tsunami INT,
    sig INT,

    net VARCHAR(20),
    code VARCHAR(50),
    ids TEXT,
    sources TEXT,
    types TEXT,

    nst FLOAT,
    dmin FLOAT,
    rms FLOAT,
    gap FLOAT,

    magType VARCHAR(10),
    type VARCHAR(30),
    title TEXT,

    longitude FLOAT,
    latitude FLOAT,
    depth_km FLOAT,

    year INT,
    month INT,
    day INT,
    hour INT,
    day_of_week VARCHAR(10),

    country VARCHAR(50),
    depth_category VARCHAR(20),
    strong_quake_flag INT,
    tsunami_flag VARCHAR(5)
);
