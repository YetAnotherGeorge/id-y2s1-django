BEGIN;

-- 1. MONEDA
INSERT INTO app_zona_agro_now_moneda (id_moneda, cod_iso, curs_schimb_ron, data_actualizare) VALUES
    (1, 'RON', 1.0000, '2026-11-26'),
    (2, 'EUR', 4.9765, '2026-11-26'),
    (3, 'USD', 4.6820, '2026-11-26'),
    (4, 'JPY', 0.0305, '2026-11-26'),
    (5, 'GBP', 5.9410, '2026-11-26')
ON CONFLICT (id_moneda) DO NOTHING;

-- 2. CATEGORIE
INSERT INTO app_zona_agro_now_categorie (id_categorie, nume, descriere, culoare, sigla, necesita_montaj_autorizat) VALUES
    (1, 'Compresor Unitate AC', 'Compresoare de aer conditionat si climatizare 12V/24V pentru cabine de tractoare, combine si excavatoare.', '#7FB069', 'fa-solid fa-snowflake', TRUE),
    (2, 'Pompa Injectie Combustibil', 'Pompe de injectie motorina de inalta presiune pentru motoare diesel agricole si industriale.', '#CA3C25', 'fa-solid fa-gas-pump', TRUE),
    (3, 'Pompa Compresor Scaun Pneumatic', 'Compresoare electrice 12V/24V pentru suspensia pneumatica a scaunelor de operator.', '#647ED3', 'fa-solid fa-chair', FALSE),
    (4, 'Filtru Hidraulic si Motor', 'Filtre de ulei hidraulic, combustibil si aer pentru intretinerea periodica a utilajelor.', '#E4DE90', 'fa-solid fa-filter', FALSE),
    (5, 'Alternator si Sistem Electric', 'Alternatoare, electromotoare si componente electrice de pornire pentru utilaje grele.', '#072020', 'fa-solid fa-car-battery', TRUE)
ON CONFLICT (id_categorie) DO NOTHING;

-- 3. BRAND_UTILAJ
INSERT INTO app_zona_agro_now_brandutilaj (id_brand, nume, tara_origine, website_oficial) VALUES
    (1, 'John Deere', 'SUA', 'https://www.deere.com'),
    (2, 'Caterpillar', 'SUA', 'https://www.caterpillar.com'),
    (3, 'Komatsu', 'Japonia', 'https://www.komatsu.com'),
    (4, 'Hitachi', 'Japonia', 'https://www.hitachicm.com'),
    (5, 'Hyundai', 'Coreea de Sud', 'https://www.hyundai-ce.com/en'),
    (6, 'Grammer', 'Germania', 'https://www.grammer.com'),
    (7, 'Kubota', 'Japonia', 'https://www.kubota.com'),
    (8, 'Bobcat', 'SUA', 'https://www.bobcat.com')
ON CONFLICT (id_brand) DO NOTHING;

-- 4. FURNIZOR
INSERT INTO app_zona_agro_now_furnizor (id_furnizor, nume_companie, tara, timp_livrare_zile, moneda_id) VALUES
    (1, 'Deere & Co. OEM Parts', 'SUA', 5, 3),
    (2, 'Gerald Elektrowerkzeuge', 'Germania', 4, 2),
    (3, 'Schnelle Teile Industrial', 'Germania', 4, 2),
    (4, 'HappyTouring Auto AC', 'Polonia', 3, 2),
    (5, 'AgroNow Direct Romania', 'Romania', 1, 1)
ON CONFLICT (id_furnizor) DO NOTHING;

-- 5. PRODUS
INSERT INTO app_zona_agro_now_produs (
    id_produs, nume, pret_bani, stoc_disponibil, tensiune_alimentare, este_original_oem, garantie_luni, data_adaugare, 
    modele_compatibile,
    categorie_id, 
    furnizor_id
) VALUES
    (
        1, 'Compresor Aer Condiționat 12V 10PA17C pentru Tractor John Deere', 307400, 12, '12V', TRUE, 24, NOW() - INTERVAL '19 days', 
        '["5520", "6403", "6603", "7600", "7610", "7630", "7700"]'::jsonb, -- categorie
        1, -- categorie id
        1 --  furnizor id
    ),
    (   
        2, 'Compresor Aer Condiționat 24V 10S15C pentru John Deere, Caterpillar și Komatsu', 72500, 25, '24V', FALSE, 12, NOW() - INTERVAL '18 days', 
        '["447220-4053", "20Y-979-6121", "447220-4052", "447220-4780", "447220-4781", "17A-911-4810"]'::jsonb, -- categorie
        1,  -- furnizor id
        5 -- categorie id
    ),
    (
        3, 'Compresor Aer Condiționat pentru Excavator Hitachi și John Deere (ZX240-3 / ZX330-3)', 55100, 18, '24V', FALSE, 12, NOW() - INTERVAL '17 days', 
        '["ZX240-3", "ZX330-3"]'::jsonb,
        1, 
        4
    ),
    (
        4, 'Pompă de Injecție Motorină DB4629-5512 / RE503049 pentru Motoare John Deere', 716800, 5, 'N/A', TRUE, 24, NOW() - INTERVAL '16 days', 
        '["3029", "4039", "4045", "4239", "6068"]'::jsonb, 
        2, 
        1
    ),
    (
        5, 'Compresor Clima AC AL154203 / RE203758 pentru Utilaje John Deere', 50100, 30, '12V', FALSE, 12, NOW() - INTERVAL '15 days', 
        '["AL154203", "AL155836", "AL176857", "RE203758", "RE257084", "447170-8931", "447100-2324", "447170-2310", "447170-2900"]'::jsonb, 
        1, 
        5
    ),
    (
        6, 'Compresor Aer Condiționat Auto RE284680 / DCP99520 pentru John Deere', 60700, 14, '12V', FALSE, 12, NOW() - INTERVAL '14 days', 
        '["RE284680", "DCP99520"]'::jsonb, 
        1, 
        4
    ),
    (
        7, 'Compresor Aer Condiționat 4621589 pentru Macara și Utilaje John Deere / Hitachi', 60200, 9, '24V', FALSE, 12, NOW() - INTERVAL '13 days', 
        '["4621589", "506012-2330", "5060122330", "5062119730", "5062117930", "787B244279"]'::jsonb, 
        1, 
        2
    ),
    (
        8, 'Compresor Aer Condiționat 10PA17C (Ansyin) pentru Tractoare John Deere Seria 7000/8000', 56800, 22, '12V', FALSE, 18, NOW() - INTERVAL '12 days', 
        '["7000/8000 SERIES", "RE46609", "AH169875", "4472003084", "4471002381", "4471002388"]'::jsonb,
        1, 
        2
    ),
    (
        9, 'Compresor Clima AC pentru Utilaje Grele John Deere, Hitachi și Hyundai', 54000, 16, '24V', FALSE, 12, NOW() - INTERVAL '11 days', 
        '["03-256-EIR", "4709228", "4721999", "FXB00001040", "503-254", "ZX870H-5G", "ZX870LC-5B"]'::jsonb, 
        1, 
        3
    ),
    (
        10, 'Compresor Aer Condiționat 10PA17C (ADANGKnight) pentru Tractoare John Deere Seria 7000/8000', 62100, 19, '12V', FALSE, 18, NOW() - INTERVAL '10 days', 
        '["7000/8000 SERIES", "RE46609", "AH169875", "4472003084", "4471002381", "4471002388"]'::jsonb, 
        1, 
        3
    ),
    (
        11, 'Compresor Aer Condiționat AH169875 / RE46609 pentru Tractor John Deere', 57300, 11, '12V', FALSE, 12, NOW() - INTERVAL '9 days', '["AH169875", "RE46609"]'::jsonb, 
        1, 
        5
    ),
    (
        12, 'Compresor Aer Condiționat 12V 10SRE18C pentru Tractor John Deere', 57900, 27, '12V', FALSE, 12, NOW() - INTERVAL '8 days', 
        '["AT367640", "SE502623", "RE284680", "447280-1650", "RE50269", "SE502697"]'::jsonb, 
        1, 
        4
    ),
    (
        13, 'Compresor Aer Condiționat 10PA17C 8PK pentru Excavator John Deere și Caterpillar', 181800, 7, '24V', TRUE, 24, NOW() - INTERVAL '7 days', 
        '["22817N", "447200-5964", "AH169875", "AN221429"]'::jsonb, 
        1, 
        1
    ),
    (
        14, 'Compresor Aer Condiționat HappyTouring AL154203 pentru Tractor John Deere', 57500, 15, '12V', FALSE, 12, NOW() - INTERVAL '6 days', 
        '["AL154203", "AL155836", "AL176857", "RE203758", "RE257084", "447100-2324", "447170-2310", "447170-2900", "447170-8931"]'::jsonb, 
        1, 
        4
    ),
    (
        15, 'Compresor Aer Condiționat 12V 10PA15C cu 8 Caneluri pentru John Deere', 61700, 20, '12V', FALSE, 12, NOW() - INTERVAL '5 days', 
        '["AL176857", "40440058", "4473000392", "4473000399", "TSP0155312"]'::jsonb, 
        1, 
        2
    ),
    (
        16, 'Compresor Aer Condiționat 12V RE502624 pentru Mașini de Erbicidat John Deere', 181700, 6, '12V', TRUE, 24, NOW() - INTERVAL '4 days', 
        '["4700", "4710", "4720", "4730", "4920", "4930", "6700"]'::jsonb, 
        1, 
        1
    ),
    (
        17, 'Compresor Aer Condiționat 10S13C pentru Excavator John Deere, Hitachi și Hyundai', 55500, 13, '24V', FALSE, 12, NOW() - INTERVAL '3 days', 
        '["03-256-EIR", "4721999", "FXB00001040", "503-254", "ZX870H-5G", "ZX870LC-5B", "4709228"]'::jsonb, 
        1, 
        3
    ),
    (
        18, 'Pompă Compresor 12V GR1220254 pentru Scaun Pneumatic Grammer (John Deere, Kubota, Bobcat)', 47600, 35, '12V', FALSE, 12, NOW() - INTERVAL '2 days', 
        '["GR1220254"]'::jsonb, 
        3, 
        5
    ),
    (
        19, 'Compresor Aer Condiționat 12V AL232176 pentru Buldoexcavator John Deere', 144800, 8, '12V', TRUE, 24, NOW() - INTERVAL '1 day', 
        '["210K EP", "310K", "310L", "315SK", "315SL"]'::jsonb, 
        1, 
        1
    )
ON CONFLICT (id_produs) DO NOTHING;

-- 6. RELATIA MANY-TO-MANY: PRODUS <-> BRAND_UTILAJ (conform coloanei Compatible Brand(s) din Readme.md)
INSERT INTO app_zona_agro_now_produs_branduri_compatibile (produs_id, brandutilaj_id) VALUES
    -- 001: John Deere
    (1, 1),
    -- 002: John Deere, Caterpillar, Komatsu
    (2, 1), (2, 2), (2, 3),
    -- 003: Hitachi, John Deere
    (3, 4), (3, 1),
    -- 004: John Deere
    (4, 1),
    -- 005: John Deere
    (5, 1),
    -- 006: John Deere
    (6, 1),
    -- 007: John Deere, Hitachi
    (7, 1), (7, 4),
    -- 008: John Deere
    (8, 1),
    -- 009: John Deere, Hitachi, Hyundai
    (9, 1), (9, 4), (9, 5),
    -- 010: John Deere
    (10, 1),
    -- 011: John Deere
    (11, 1),
    -- 012: John Deere
    (12, 1),
    -- 013: John Deere, Caterpillar
    (13, 1), (13, 2),
    -- 014: John Deere
    (14, 1),
    -- 015: John Deere
    (15, 1),
    -- 016: John Deere
    (16, 1),
    -- 017: John Deere, Hitachi, Hyundai
    (17, 1), (17, 4), (17, 5),
    -- 018: Grammer, John Deere, Kubota, Bobcat
    (18, 6), (18, 1), (18, 7), (18, 8),
    -- 019: John Deere
    (19, 1)
ON CONFLICT DO NOTHING;

-- 7. IMAGINE_PRODUS
INSERT INTO app_zona_agro_now_imagineprodus (id, produs_id, numar_ordine, cale_fisier, este_principala) VALUES
    (1, 1, 1, 'img/db-produse/products/product_001.jpg', TRUE),
    (2, 2, 1, 'img/db-produse/products/product_002.jpg', TRUE),
    (3, 3, 1, 'img/db-produse/products/product_003.jpg', TRUE),
    (4, 4, 1, 'img/db-produse/products/product_004.jpg', TRUE),
    (5, 5, 1, 'img/db-produse/products/product_005.jpg', TRUE),
    (6, 6, 1, 'img/db-produse/products/product_006.jpg', TRUE),
    (7, 7, 1, 'img/db-produse/products/product_007.jpg', TRUE),
    (8, 8, 1, 'img/db-produse/products/product_008.jpg', TRUE),
    (9, 9, 1, 'img/db-produse/products/product_009.jpg', TRUE),
    (10, 10, 1, 'img/db-produse/products/product_010.jpg', TRUE),
    (11, 11, 1, 'img/db-produse/products/product_011.jpg', TRUE),
    (12, 12, 1, 'img/db-produse/products/product_012.jpg', TRUE),
    (13, 13, 1, 'img/db-produse/products/product_013.jpg', TRUE),
    (14, 14, 1, 'img/db-produse/products/product_014.jpg', TRUE),
    (15, 15, 1, 'img/db-produse/products/product_015.jpg', TRUE),
    (16, 16, 1, 'img/db-produse/products/product_016.jpg', TRUE),
    (17, 17, 1, 'img/db-produse/products/product_017.jpg', TRUE),
    (18, 18, 1, 'img/db-produse/products/product_018.jpg', TRUE),
    (19, 19, 1, 'img/db-produse/products/product_019.jpg', TRUE)
ON CONFLICT (id) DO NOTHING;

COMMIT;
