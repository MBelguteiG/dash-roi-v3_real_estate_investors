"""Page text in English and Mongolian. Each entry: key: (English, Монгол)."""

LANG_NAMES = {"en": "English", "mn": "Монгол"}

TEXT = {
    # --- top bar ---
    "strategy": ("Investment strategy", "Хөрөнгө оруулалтын стратеги"),
    "scenario": ("Scenario", "Хувилбар"),
    "model_Rental": ("Rental", "Түрээсийн байр"),
    "model_BRRR": ("BRRR", "АЗТД"),
    "model_Flip": ("Flip", "Засаад зарах"),
    "sc_Conservative": ("Conservative", "Гутранги"),
    "sc_Base": ("Base", "Суурь"),
    "sc_Aggressive": ("Aggressive", "Өөдрөг"),

    # --- quick start ---
    "quick_start": ("Quick start", "Ашиглалтын заавар"),
    "quick_body": (
        "1. **Pick a model and scenario** in the top bar: Rental, BRRR or Flip; "
        "Conservative, Base or Aggressive.\n"
        "2. **Enter the deal.** Press Enter after typing a number, or use − and +.\n"
        "3. **Read the verdict.** The tiles give the headline numbers; "
        "Investor view explains the verdict and what would fix it. "
        "Lender view shows how a lender sizes the loan and whether it is likely to fund.\n"
        "4. **Most you should pay** is the most you can pay and still meet your target "
        "(for Flip, the max allowable offer).",
        "1. **Хөрөнгө оруулалтын стратеги болон хувилбараа сонгоно уу** (дээд мөрөнд): "
        "Түрээсийн байр, АЗТД (Авах → Засах → Түрээслүүлэх → Дахин санхүүжүүлэх) "
        "эсвэл Засаад зарах, Гутранги, Суурь эсвэл Өөдрөг.\n"
        "2. **Үл хөдлөх эд хөрөнгийн мэдээллээ оруулна уу.** Мэдээлэлээ бичсэний дараа Enter дарах, "
        "эсвэл − болон + товч ашиглана.\n"
        "3. **Шийдвэрийг уншина уу.** Танд санхүүгийн үзүүлэлтүүдийг харуулна. "
        "Хөрөнгө оруулагчийн хувьд шийдвэрийн шалтгаан болон мөн ямар хүчин зүйлийг өөрчилбөл "
        "та хөрөнгө оруулалтын зорилгодоо хүрэхийг тайлбарлана. Зээлдүүлэгчийн хувьд банк зээлийг хэрхэн тооцож, "
        "зээл олгох магадлалыг харуулна.\n"
        "4. **Төлж болох дээд үнэ** нь таны хүсэж байгаа хөрөнгө оруулалтын өгөөжийн зорилтыг хангах дээд үнэ "
        "(Засаад зарах үед: засвар, зээл, эзэмших болон борлуулалтын зардлын дараа ашгийн зорилтдоо хүрэхийн тулд худалдагчид санал болгох хамгийн өндөр үнэ).",
    ),

    # --- dropdown options ---
    "st_Illinois": ("Illinois", "Иллинойс"),
    "st_California": ("California", "Калифорни"),
    "pt_SFH": ("SFH", "Хаус"),
    "pt_Condo": ("Condo", "Кондо (орон сууц)"),
    "pt_Townhouse": ("Townhouse", "Таунхаус"),
    "pt_Duplex": ("Duplex", "Хоёр айлын байшин"),
    "rt_Cash-Out": ("Cash-Out", "Бэлэн мөнгө гаргаж авах"),
    "rt_Rate/Term": ("Rate/Term", "Зөвхөн зээлийн нөхцөл солих"),

    # --- input labels ---
    "state": ("State", "Муж"),
    "type": ("Type", "Төрөл"),
    "price": ("Price", "Үнэ"),
    "down": ("Down payment %", "Урьдчилгаа төлбөр %"),
    "rate": ("Loan rate %", "Зээлийн хүү %"),
    "rent": ("Rent / mo", "Түрээс / сар"),
    "years": ("Years you'll own it", "Эзэмших хугацаа (жил)"),
    "goal": ("Return goal %", "Өгөөжийн зорилт %"),
    "rehab": ("Repair budget", "Засварын төсөв"),
    "arv": ("Value after repairs", "Засварын дараах үнэ цэнэ"),
    "arv_flip": ("Sale price after repairs", "Засварын дараах зарах үнэ"),
    "hm_ltv": ("Short-term loan %", "Богино хугацааны зээл %"),
    "hm_rate": ("Short-term rate %", "Богино хугацааны зээлийн хүү %"),
    "refi_month": ("Months to refinance", "Дахин санхүүжүүлэх сар"),
    "refi_ltv": ("New loan % of value", "Зээл, байрны үнэлгээний харьцаа %"),
    "post_rate": ("New loan rate %", "Шинэ зээлийн хүү %"),
    "refi_type": ("Refinance type", "Дахин санхүүжилтийн төрөл"),
    "hold": ("Months to fix and sell", "Засах болон зарах хугацаа (сар)"),
    "profit_goal": ("Profit goal %", "Ашгийн зорилт %"),
    "lender_fee": ("Lender fee %", "Зээлдүүлэгчийн шимтгэл %"),
    "utilities": ("Utilities / mo", "Ашиглалтын зардал / сар"),
    "upkeep": ("Upkeep & security / mo", "Арчилгаа, хамгаалалт / сар"),
    "hoa": ("HOA / mo", "СӨХ төлбөр / сар"),
    "hoa_default": ("default {x}", "үндсэн {x}"),
    "start_title": ("Enter your deal to see the numbers",
                    "Тооцоог харахын тулд мэдээллээ оруулна уу"),
    "start_note": ("Every box starts empty: nothing is filled in for you. Type 0 where a "
                   "cost doesn't apply. HOA, property tax and insurance can stay empty to "
                   "use the state average.",
                   "Бүх талбар хоосон эхэлнэ. Хамаарахгүй зардлын талбарт 0 гэж бичнэ үү. "
                   "СӨХ төлбөр, татвар, даатгалын талбарыг хоосон орхивол муж улсын "
                   "дундажийг ашиглана."),
    "start_missing": ("Still empty: {x}", "Хоосон байгаа талбар: {x}"),
    "dscr_min": ("Minimum DSCR", "Түрээс / сарын төлбөрийн доод харьцаа"),
    "tax_yr": ("Property tax / yr", "Үл хөдлөх эд хөрөнгийн албан татвар / жил"),
    "ins_yr": ("Insurance / yr", "Даатгал / жил"),
    "points": ("Points to lower rate", "Хүү бууруулах оноо (points)"),
    "fees": ("Lender fees", "Зээлийн шимтгэл, хураамж"),

    # --- input help notes (the ? icons) ---
    "h_price": ("What you pay for the property.",
                "Үл хөдлөх хөрөнгөнд төлөх үнэ."),
    "h_price_before": ("What you pay for the property before repairs.",
                       "Засварлахаас өмнө худалдаж авах үнэ."),
    "h_down": ("Cash you put down, as a % of the price. The rest is the loan.",
               "Үнийн хэдэн хувийг бэлнээр төлөх вэ. Үлдсэнийг зээлээр санхүүжүүлнэ."),
    "h_rate": ("Yearly interest rate on the loan, before any points.",
               "Зээлийн жилийн хүү (оноо худалдаж авахаас өмнөх)."),
    "h_rent": ("Monthly rent you expect to collect.",
               "Сар бүр түрээслэхээр тооцож буй түрээсийн төлбөр."),
    "h_rent_brrr": ("Monthly rent once it's fixed up and rented.",
                    "Засвар дуусч түрээслэсний дараах сарын түрээс."),
    "h_years": ("When you plan to sell.", "Хэдэн жилийн дараа зарахаар төлөвлөж байна."),
    "h_goal": ("The yearly return you want on the cash you put in.",
               "Оруулсан хөрөнгө оруулалтаасаа хүсч буй жилийн өгөөж."),
    "h_rehab": ("What you expect to spend fixing it up.",
                "Засварт зарцуулахаар тооцож буй мөнгө."),
    "h_arv": ("What it should be worth once fixed up (ARV).",
              "Засвар дууссаны дараах зах зээлийн үнэ цэнэ."),
    "h_arv_flip": ("What you expect to sell it for once fixed up (ARV).",
                   "Засвар дууссаны дараа зарна гэж тооцож буй үнэ."),
    "h_hm_ltv": ("The short-term (hard money) loan as a % of the price. Usually 70–90%. "
                 "Ask your lender.",
                 "Богино хугацааны (hard money) зээл, үнийн хувиар. Ихэвчлэн 70–90%. "
                 "Зээлдүүлэгчээсээ лавлана уу."),
    "h_hm_rate": ("Yearly interest on the short-term loan. You pay interest only. "
                  "Usually 10–14%. Ask your lender.",
                  "Богино хугацааны зээлийн жилийн хүү. Зөвхөн хүүг нь төлнө. "
                  "Ихэвчлэн 10–14%. Зээлдүүлэгчээсээ лавлана уу."),
    "h_refi_month": ("When you swap the short-term loan for a regular 30-year loan. Usually "
                     "6–12 months; many lenders want about 6 months of ownership first. "
                     "Must be before you sell.",
                     "Богино хугацааны зээлийг ердийн 30 жилийн зээлээр солих хугацаа. "
                     "Ихэвчлэн 6–12 сар; олон банк эхлээд 6 орчим сар эзэмшсэн байхыг "
                     "шаарддаг. Зарахаас өмнө байх ёстой."),
    "h_refi_ltv": ("The new 30-year loan as a % of the value after repairs. Usually 70–75% "
                   "for a cash-out refinance. Ask your lender.",
                   "Шинэ 30 жилийн зээлийн дүнг засварын дараах үнэлгээнд харьцуулсан хувь (ЗҮХ). "
                   "Бэлэн мөнгө гаргаж авах дахин санхүүжилтэд ихэвчлэн 70–75%. "
                   "Банкаасаа лавлана уу."),
    "h_post_rate": ("Yearly interest rate on the new 30-year loan. Use the rate your lender "
                    "quotes today; rates change often.",
                    "Шинэ 30 жилийн зээлийн жилийн хүү. Банкны өнөөдрийн санал болгож буй "
                    "хүүг оруулна уу; хүү байнга өөрчлөгддөг."),
    "h_refi_type": ("Cash-Out: borrow the full % and take cash back out. "
                    "Rate/Term: borrow only enough to pay off the short-term loan.",
                    "Дахин санхүүжилт (бэлэн мөнгө гаргаж авах): зээлийг бүтэн хувиар авч, бэлэн мөнгө буцааж авна. "
                    "Дахин санхүүжилт (зөвхөн зээлийн нөхцөл солих): зөвхөн богино хугацааны зээлээ төлөх хэмжээгээр зээлнэ."),
    "h_hold": ("From buying to selling.", "Худалдаж авснаас зарах хүртэлх хугацаа."),
    "h_profit_goal": ("The profit you want, as a % of the sale price.",
                      "Зарах үнийн хувиар хүсч буй ашиг."),
    "h_lender_fee": ("Up-front fee (points) the short-term lender charges, as a % of the loan.",
                     "Богино хугацааны зээлдүүлэгчийн урьдчилан авах шимтгэл (points), зээлийн хувиар."),
    "h_utilities": ("Power, water and gas while you own it.",
                    "Эзэмших хугацааны цахилгаан, ус, хийн зардал."),
    "h_upkeep": ("Lawn, cleaning, locks and alarms while it's empty.",
                 "Сул байх үеийн зүлэг, цэвэрлэгээ, цоож, дохиоллын зардал."),
    "h_dscr_min": ("The lowest DSCR (rent ÷ PITIA) your lender will accept. For 1–4 unit "
                   "rentals, Fannie Mae and Freddie Mac don't use DSCR; DSCR loans come from "
                   "private lenders, who set their own minimum, often 1.00. For apartment "
                   "buildings with 5 or more units, Fannie Mae and Freddie Mac want at least "
                   "1.25x (Freddie Mac: 1.20x in top markets), counted as rent left after "
                   "expenses and repair reserves ÷ yearly loan payment. Ask your lender.",
                   "Банкны зөвшөөрдөг хамгийн бага харьцаа (түрээсийн төлбөр ÷ мортгэйжийн сарын төлбөр). 1–4 айлын "
                   "түрээсийн байранд Fannie Mae, Freddie Mac энэ харьцааг ашигладаггүй; ийм "
                   "зээлийг хувийн зээлдүүлэгчид олгодог бөгөөд доод харьцааг өөрсдөө "
                   "тогтоодог, ихэвчлэн 1.00. 5 ба түүнээс дээш айлын орон сууцны барилгад "
                   "Fannie Mae, Freddie Mac хамгийн багадаа 1.25x (Freddie Mac: томоохон зах "
                   "зээлд 1.20x) шаарддаг бөгөөд үүнийг зардлын дараах түрээсийн орлого ÷ "
                   "зээлийн төлбөрөөр тооцдог. Банкнаасаа лавлана уу."),
    "h_tax_yr": ("Leave blank to use the state average. Type the exact yearly tax "
                 "for this property if you know it.",
                 "Хоосон орхивол муж улсын дундажийг ашиглана. Энэ үл хөдлөх эд хөрөнгийн "
                 "жилийн татварыг мэдэж байвал яг дүнгээр нь оруулна уу."),
    "h_ins_yr": ("Leave blank to use the state average. Type your insurance quote "
                 "for this property if you have one.",
                 "Хоосон орхивол муж улсын дундажийг ашиглана. Энэ үл хөдлөх эд хөрөнгийн "
                 "даатгалын үнийн саналтай бол оруулна уу."),
    "h_hoa": ("Leave blank to use the state and property-type default.",
              "Хоосон орхивол муж болон байрны төрлийн үндсэн дүнг ашиглана."),
    "h_fees": ("Optional. What the lender charges to make the loan (for BRRR, the new loan): "
               "origination, underwriting, processing. Used only for the estimated APR, "
               "for comparing loan offers. Your returns already include these in the closing "
               "costs (for BRRR, in the refinance closing costs). Title, appraisal "
               "and recording fees don't count toward APR.",
               "Заавал биш. Зээлдүүлэгчийн зээл олгоход авах шимтгэл, хураамж (BRRR-д шинэ "
               "зээлийн): зээл олгох, зээлийн шинжилгээ, бүрдүүлэлтийн. Зөвхөн зээлийн бодит "
               "өртгийг тооцож, зээлийн саналуудыг харьцуулахад ашиглана. Таны өгөөжийн "
               "тооцоонд эдгээр нь худалдан авахтай холбоотой зардалд (BRRR-д дахин "
               "санхүүжилтийн зардалд) аль хэдийн орсон. Өмчлөх эрхийн "
               "даатгал, үнэлгээ, бүртгэлийн хураамж зээлийн бодит өртөгт орохгүй."),
    "h_points": ("Each point costs 1% of the loan (for BRRR, the new loan) "
                 "and lowers your rate by about 0.25%.",
                 "Нэг оноо зээлийн 1%-тай тэнцэх үнэтэй (BRRR-д шинэ зээлийн) "
                 "бөгөөд хүүг ойролцоогоор 0.25%-иар бууруулна."),

        # --- verdict + tiles ---
    "verdict": ("Investor verdict", "Хөрөнгө оруулагчийн шийдвэр"),
    "v_HARD REJECT": ("HARD REJECT", "Шууд татгалзах"),
    "v_REJECT": ("REJECT", "Татгалзах"),
    "v_NEGOTIATE": ("NEGOTIATE", "Нөхцөл тохиролцох"),
    "v_ACCEPT": ("ACCEPT", "Худалдан авах"),
    "v_BUY": ("BUY", "Худалдан авах"),
    "v_why_dscr": ("Lender won't fund: rent ÷ PITIA {d}x is below {m}x",
                   "Банк зээл олгохгүй: түрээс / сарын төлбөрийн харьцаа {d}x, доод шаардлага {m}x"),
    "t_return": ("Yearly return", "Жилийн өгөөж"),
    "t_dscr": ("DSCR (rent ÷ PITIA)", "Түрээс / сарын төлбөрийн харьцаа"),
    "t_coc": ("First-year cash return", "Эхний жилийн бэлэн мөнгөний өгөөж"),
    "t_cash_left": ("Your money still in the property", "Үлдэгдэл хөрөнгө оруулалт"),
    # --- BRRR cost breakdown (Nov 24, 2026) ---
    "bk_purchase": ("At purchase", "Худалдан авахад"),
    "bk_down": ("Down payment (price − short-term loan)",
                "Урьдчилгаа төлбөр (үнэ − богино хугацааны зээл)"),
    "bk_rehab": ("While repairing ({m} months, paid monthly)",
                 "Засварын үед ({m} сар, сар бүр төлнө)"),
    "bk_hm_int": ("Short-term loan interest", "Богино хугацааны зээлийн хүү"),
    "bk_carry": ("Property tax, insurance, HOA (no rent yet)",
                 "Үл хөдлөх хөрөнгийн албан татвар, даатгал, СӨХ төлбөр (түрээсгүй үе)"),
    "bk_rehab_total": ("Paid while repairing", "Засварын үед төлсөн"),
    "bk_refi": ("At the refinance (month {m})", "Дахин санхүүжилтийн үед ({m} {o} сар)"),
    "bk_payoff": ("Pay off the short-term loan", "Богино хугацааны зээлийг төлөх"),
    "bk_refi_cost": ("Refinance closing costs ({x}, includes lender fees)",
                     "Дахин санхүүжилтийн зардал ({x}, зээлийн шимтгэл, хураамжийг багтаасан)"),
    "bk_note": ("What you pay while repairing comes from your pocket too. It isn't in "
                "\"money still in the property\", but it is counted in the yearly return "
                "and the cash flow table. Your equity is not cash you pay: it comes back "
                "to you when you sell, as cash from the sale.",
                "Засварын үед төлсөн зардлыг мөн өөрийн мөнгөөр төлнө. Энэ нь үлдэгдэл "
                "хөрөнгө оруулалтад ороогүй ч жилийн өгөөж болон мөнгөн гүйлгээний "
                "хүснэгтэд тооцогдсон. Өөрийн хөрөнгө нь таны төлөх мөнгө биш: зарах үед "
                "борлуулалтаас орох мөнгө болж танд буцаж ирнэ."),
    "bk_eq_head": ("Your equity after the refinance",
                   "Дахин санхүүжилтийн дараах таны өөрийн хөрөнгө"),
    "bk_equity": ("Your equity (value − new loan)", "Таны өөрийн хөрөнгө (байрны үнэ цэнэ − шинэ зээл)"),
    "bk_eq_left": ("of which: your money still in", "үүнээс: таны оруулсан үлдэгдэл хөрөнгө оруулалт"),
    "bk_eq_extra": ("of which: cash taken out beyond what you put in",
                    "үүнээс: оруулснаас илүү гаргаж авсан мөнгө"),
    "bk_eq_created": ("of which: value the repairs created",
                      "үүнээс: засвараар бий болсон үнэ цэнэ"),
    "t_margin": ("Profit as % of sale price", "Ашиг, зарах үнийн %"),
    "t_net_profit": ("Net profit", "Цэвэр ашиг"),
    "t_max_pay": ("Most you should pay", "Төлж болох дээд үнэ"),
    "c_goal": ("your goal {x}%", "таны зорилт {x}%"),
    "c_bank": ("your lender minimum {m}x", "банкны шаардах доод харьцаа {m}x"),
    "c_pitia": ("rent {rent} ÷ PITIA {pitia}", "түрээс {rent} ÷ сарын төлбөр {pitia}"),
    "c_coc": ("of the cash you put in", "оруулсан бэлэн мөнгөнөөс"),
    "c_coc_amt": ("of the {x} you put in", "оруулсан {x} бэлэн мөнгөнөөс"),
    "b_down": ("Down payment", "Урьдчилгаа төлбөр"),
    "b_closing": ("Closing costs", "Худалдан авахтай холбоотой зардал"),
    "b_repairs": ("Repairs", "Засварын зардал"),
    "b_points": ("Points", "Хүү бууруулах оноо"),
    "all_cash_out": ("All cash out", "Оруулсан мөнгөө бүрэн буцааж авсан"),
    "c_no_cash_left": ("no cash left in the deal", "хөрөнгө оруулалтаа бүрэн гаргаж авсан"),
    "c_refi_more": ("You got all your money back, plus {x}",
                    "Оруулсан мөнгөө бүрэн буцааж авсан, нэмээд {x}"),
    "c_of_invested": ("You put in {x}; refinance gave back {y}",
                      "Та {x} оруулсан; дахин санхүүжилтээр {y} буцааж авсан"),
    "c_flip_months": ("{n}-month flip, as a yearly rate", "{n} сарын өгөөжийг жилээр тооцсон"),
    "c_holding": ("holding {x} / mo", "эзэмших зардал {x} / сар"),
    "c_vs_asking": ("vs {x} asking", "худалдагчийн зарах үнэ {x}"),
    "c_bank_sets": ("the bank test sets this · asking {x}", "худалдагчийн зарах үнэ {x}"),
    "c_goal_sets": ("your goal sets this · asking {x}", "худалдагчийн зарах үнэ {x}"),
                 
    "c_price_cant_fix": ("based on your goal: Most you should pay can't fix the bank test",
                         "Таны зорилгод үндэслэсэн: Төлж болох дээд үнээр банкны шалгуурыг засах боломжгүй"),
    "na": ("n/a", "Хамаарахгүй"),
    "c_all_back": ("you get all your cash back at refi",
                   "дахин санхүүжилтээр бүх мөнгөө буцааж авна"),
    "none": ("none", "Байхгүй"),
    "c_no_price": ("no price meets the target", "зорилтод хүрэх үнэ байхгүй"),

    # --- pop-ups ---
    "what_mean": ("What does this mean?", "Энэ юу гэсэн үг вэ?"),
    "p_return": (
        "**{irr} a year** is your average yearly return on the cash you put in.\n\n"
        "**After inflation: {real} a year.** Prices rise about {infl} a year, so future "
        "dollars buy less. This is what your return is worth in today's money.\n\n"
        "**Total profit over {years} years:** {profit}, or {real_profit} in today's dollars.",
        "**Жилд {irr}** нь таны оруулсан бэлэн мөнгөний дундаж жилийн өгөөж.\n\n"
        "**Инфляцийн дараа: жилд {real}.** Үнэ жилд ойролцоогоор {infl}-иар өсөх тул "
        "ирээдүйн доллараар бага зүйл худалдан авна. Энэ нь таны өгөөжийн өнөөгийн "
        "мөнгөөр илэрхийлсэн үнэ цэнэ.\n\n"
        "**{years} жилийн нийт ашиг:** {profit}, өнөөгийн мөнгөөр {real_profit}.",
    ),
    "when_rental": ("in year 1", "эхний жилд"),
    "when_brrr": ("after the refi", "дахин санхүүжилтийн дараа"),
    "p_dscr": (
        "This is how DSCR lenders measure it, {when}: monthly rent **{rent}** ÷ PITIA "
        "**{pitia}** = **{x}x**.\n\n"
        "PITIA = loan payment {pi} + property tax {tax} + insurance {ins} + HOA {hoa}.\n\n"
        "Your lender minimum is **{m}x**; 1.25x is strong. Below 1.00x, the rent doesn't "
        "cover the monthly payment.",
        "Банк үүнийг {when} ингэж тооцдог: сарын түрээс **{rent}** ÷ сарын төлбөр "
        "**{pitia}** = **{x}x**.\n\n"
        "Сарын төлбөр = зээлийн үндсэн төлбөр ба хүү {pi} + үл хөдлөх эд хөрөнгийн албан "
        "татвар {tax} + даатгал {ins} + СӨХ төлбөр {hoa}.\n\n"
        "Банкны шаардах доод харьцаа **{m}x**; 1.25x бол хангалттай. 1.00x-ээс бага бол "
        "түрээс сарын төлбөрийг бүрэн нөхөхгүй.",
    ),
    "p_coc_pos": (
        "In year 1 you keep **{x}** of the cash you put in, after the loan, expenses and "
        "money set aside for big repairs.",
        "Эхний жилд зээлийн төлбөр, холбогдох зардал болон засварын нөөцийг хассаны дараа "
        "танд ойролцоогоор **{amt}** үлдэнэ. Энэ нь таны оруулсан бэлэн мөнгөний **{x}** юм.",
    ),
    "p_coc_neg": (
        "In year 1 the rent doesn't cover everything: you add about **{x}** of the cash you "
        "put in, to pay the loan, expenses and money set aside for big repairs.",
        "Эхний жилд түрээсийн орлого зээлийн төлбөр, холбогдох зардал болон засварын нөөцийг "
        "нөхөхгүй тул та өөрийн мөнгөнөөс ойролцоогоор **{amt}** нэмж төлнө. Энэ нь таны оруулсан "
        "бэлэн мөнгөний **{x}** юм.",
    ),
    "g_rental": ("hits your {x}% goal and passes the bank test",
                 "таны {x}% зорилтод хүрч, банкны шалгуурыг давах"),
    "g_brrr": ("still hits your {x}% goal", "таны {x}% зорилтод хүрэх"),
    "g_flip": ("still leaves your target profit after repairs, loan and selling costs",
               "засвар, зээл, борлуулалтын зардлын дараа зорилтот ашгаа хадгалах"),
    "p_max": ("**{price}** is the highest price that {goal}. Pay more and the numbers stop working.",
              "**{price}** бол {goal} хамгийн өндөр үнэ. Үүнээс илүү төлбөл тооцоо таарахгүй."),
    "pm_goal": ("The seller is asking **{asking}**. Don't pay more than **{price}**: above that, "
                "your yearly return falls below your **{goal}%** goal.",
                "Худалдагчийн зарах үнэ **{asking}**. Таны төлөх дээд үнэ **{price}**: "
                "үүнээс их төлбөл жилийн өгөөж таны **{goal}%** зорилтод хүрэхгүй."),
    "pm_bank": ("The seller is asking **{asking}**. Don't pay more than **{price}**: above that, "
                "the loan gets too big and fails the bank test (rent must cover PITIA {m}x).",
                "Худалдагчийн зарах үнэ **{asking}**. Таны төлөх дээд үнэ **{price}**: "
                "үүнээс их төлбөл зээл томорч, банкны шалгуурыг (түрээс / сарын төлбөрийн "
                "харьцаа {m}x) давахгүй."),
    "pm_flip": ("The seller is asking **{asking}**. Don't offer more than **{price}**: above that, "
                "after repairs, loan, holding and selling costs your profit falls below your "
                "**{goal}%** goal.",
                "Худалдагчийн зарах үнэ **{asking}**. Таны санал болгох дээд үнэ **{price}**: "
                "үүнээс их төлбөл засвар, зээл, эзэмших болон борлуулалтын зардлын дараа ашиг "
                "таны **{goal}%** зорилтод хүрэхгүй."),

    # --- points sentence ---
    "p_points": (
        "Paying **{cost}** lowers your rate from {frm}% to **{to}%** and saves **{save} a month**. "
        "The monthly savings pay it back in **{be} months** (you plan to hold {hold}).",
        "**{cost}** төлснөөр хүү {frm}%-иас **{to}%** болж буурч, сард **{save}** хэмнэнэ. "
        "Сарын хэмнэлт үүнийг **{be} сард** нөхнө (та {hold} сар эзэмшихээр төлөвлөж байна).",
    ),
    "p_worth": (" Worth it.", " Ашигтай."),
    "p_no_fund": (
        " Even with points, rent ÷ PITIA is {d1}x, still below your lender's minimum of "
        "{m}x, so these points don't get this deal funded.",
        " Оноотой ч түрээс / сарын төлбөрийн харьцаа {d1}x байх тул банкны доод "
        "шаардлагыг ({m}x) хангахгүй. Иймд эдгээр оноо зээл авах боломжийг бүрдүүлэхгүй.",
    ),
    "p_fund": (
        " Without points, rent ÷ PITIA would be {d0}x, below your lender's minimum of "
        "{m}x. With them it's {d1}x: these points are what get this deal funded.",
        " Оноогүй бол түрээс / сарын төлбөрийн харьцаа {d0}x байх тул банкны доод "
        "шаардлагыг ({m}x) хангахгүй. Оноотой бол {d1}x болж хангана: энэ оноо л зээл "
        "авах боломжийг бүрдүүлж байна.",
    ),
    "p_not_worth": (
        " The monthly savings alone won't repay it before you sell. A lower rate also pays "
        "down more of your loan, so check your Yearly return above to see the full effect.",
        " Та зарахаасаа өмнө оноонд төлсөн мөнгөө сарын хэмнэлтээр буцааж олж амжихгүй. "
        "Гэхдээ зарах үед зээлийн үлдэгдэл бага байх тул Жилийн өгөөжийг харна уу.",
    ),

    # --- tabs ---
    "tab_inv": ("Investor view", "Хөрөнгө оруулагчийн хувьд"),
    "tab_lend": ("Lender view", "Зээлдүүлэгчийн хувьд"),
    "tab_sens": ("Sensitivity", "Өгөөжид нөлөөлөх хүчин зүйлс"),
    "tab_cf": ("Cash flow table", "Мөнгөн гүйлгээний хүснэгт"),

    # --- investor view ---
    "why": ("Why this verdict", "Шийдвэрийн шалтгаан"),
    "fix": ("What would make it work", "Юуг өөрчилбөл болох вэ"),
    "k_profit": ("Profit test: {x} after all costs", "Ашгийн шалгуур: бүх зардлын дараа {x}"),
    "k_min_profit": ("Minimum profit test: {x} of the sale price. Needs at least 10%.",
                     "Ашгийн доод хязгаар: зарах үнийн {x}. Дор хаяж 10% байх ёстой."),
    "k_profit_goal": ("Profit goal: {x} of the sale price. Your goal is {goal}%.",
                      "Ашгийн зорилт: зарах үнийн {x}. Таны зорилт {goal}%."),
    "k_bank": ("Bank test: rent ÷ PITIA is {x}x. Your lender minimum is {m}x.",
               "Банкны шалгуур: түрээс / сарын төлбөрийн харьцаа {x}x. "
               "Банкны шаардах доод харьцаа {m}x."),
    "k_return_aco": ("Return test: the refi gives back all the cash you put in",
                    "Өгөөж зорилтод хүрсэн эсэх: дахин санхүүжилтээр оруулсан бүх мөнгөө буцааж авна"),
    "k_return": ("Return test: {x} a year. Your goal is {goal}%.",
                "Өгөөж зорилтод хүрсэн эсэх: жилд {x}. Таны зорилт {goal}%."),
    "k_repairs": ("Repairs test (yours, not the bank's): after saving for big repairs, "
                  "rent covers the loan {x}x",
                  "Засварын зардлыг даах эсэх (банкных биш, таных): томоохон засварт мөнгө "
                  "хуримтлуулсны дараа түрээс зээлийг {x}x нөхнө"),
    "k_repairs_low": (". Below 1.00x, you'd add your own money for big repairs.",
                      ". 1.00x-ээс доош бол томоохон засварт өөрийн мөнгө нэмнэ."),
    "f_mao_below": ("Most you should offer: **{mao}**, {x} below the asking price",
                    "Санал болгох дээд үнэ: **{mao}**, худалдагчийн зарах үнээс {x} бага"),
    "f_mao_under": ("Most you should offer: **{mao}**. The asking price is already {x} under it",
                    "Санал болгох дээд үнэ: **{mao}**. Худалдагчийн үнэ үүнээс {x} аль хэдийн бага"),
    "f_rent_bank": ("Rent the bank needs to see: **{x}**", "Банкны шаардах түрээс: **{x}**"),
    "f_rent_repairs": ("Rent to also cover big repairs: **{x}**",
                       "Томоохон засварын нөөцийг түрээсийн төлбөрт нэмсэн дүн: **{x}**"),
    "f_max_goal": ("Most you can pay to hit your {goal}% goal: **{x}**",
                   "{goal}% зорилтод хүрэх дээд үнэ: **{x}**"),
    "f_max_bank": ("Most you can pay to pass the bank test: **{x}**",
                   "Банкны шалгуурыг давах дээд үнэ: **{x}**"),
    "f_aco": ("Price where the refi gives back all your cash: **{x}**",
              "Дахин санхүүжилтээр бүх мөнгөө буцааж авах үнэ: **{x}**"),

# --- lender view ---
    "l_loan": ("Loan amount", "Зээлийн дүн"),
    "c_of_price": ("{x} of the price", "үнийн {x}"),
    "l_noi": ("Rent left after expenses", "Зардлын дараах түрээсийн орлого"),
    "c_noi": ("year 1, before the loan payment", "эхний жил, зээлийн төлбөрөөс өмнө"),
    "l_debt": ("Loan payments / yr", "Зээлийн төлбөр / жил"),
    "c_fixed": ("{x}% fixed, 30 years", "{x}% тогтмол хүү, 30 жил"),
    "c_apr": ("estimated APR {x}", "зээлийн бодит өртөг {x} (тооцоолсон)"),
    "c_bank_strong": ("rent {rent} ÷ PITIA {pitia}; minimum {m}x",
                      "түрээс {rent} ÷ сарын төлбөр {pitia}; доод харьцаа {m}x"),
    "note_rental": ("Your rent ÷ PITIA is {d}x and the loan is {ltv} of the price. "
                    "{s}x or more and a loan of 80% or less: a lender is likely to fund it. "
                    "{m}x or more: a lender may fund it with extra conditions. "
                    "Under {m}x: a lender won't fund it.",
                    "Таны түрээс / сарын төлбөрийн харьцаа {d}x, зээл үнийн {ltv}. "
                    "Харьцаа {s}x буюу түүнээс дээш, зээл үнийн 80 хувиас хэтрэхгүй бол банк "
                    "зээл олгох магадлал өндөр. Харьцаа {m}x буюу түүнээс дээш бол банк нэмэлт "
                    "шаардлага тавьж зээл олгож болзошгүй. Харьцаа {m}x хүрэхгүй бол банк зээл олгохгүй."),    "l_cap": ("Cap rate", "Капиталжуулалтын түвшин"),
    "c_cap": ("rent left after expenses ÷ price", "зардлын дараах түрээсийн орлого ÷ үнэ"),
    "p_cap": (
        "**Cap rate** shows what the property earns if you paid the full price in cash, "
        "with no loan: rent left after year-1 expenses **{noi}** ÷ price **{price}** "
        "= **{x}** a year.\n\n"
        "The loan is left out on purpose: every buyer's loan is different, but the "
        "property's cap rate is the same for everyone. Use it to compare properties in "
        "the same area: a higher cap rate means more income for the price.",
        "**Капиталжуулалтын түвшин** нь худалдагчийн зарах үнийг бүхэлд нь бэлнээр төлж, зээл аваагүй үед "
        "үл хөдлөх эд хөрөнгө жилд хэдэн хувийн орлого олохыг харуулна: эхний жилийн "
        "зардлын дараах түрээсийн орлого **{noi}** ÷ үнэ **{price}** = **{x}**.\n\n"
        "Хүн бүрийн зээл өөр байдаг тул зээлийг оруулаагүй. Ингэснээр ойролцоо "
        "байршилтай үл хөдлөх эд хөрөнгүүдийг хооронд нь харьцуулж болдог: хувь өндөр байх "
        "тусам үнэдээ харьцуулахад орлого их юм.",
    ),
    "l_new_loan": ("New loan", "Шинэ зээл"),
    "c_on_arv": ("on a value after repairs of {x}", "засварын дараах {x} үнэ цэнэд"),
    "l_refi_ltv": ("New loan % of value", "Зээл, байрны үнэлгээний харьцаа"),
    "c_refi_at": ("{type}, refinance at month {m}", "Дахин санхүүжилтээр ({type}), {m} {o} сард"),
    "l_cash_back": ("Cash back at refinance", "Дахин санхүүжилтээр гаргаж авсан бэлэн мөнгө"),
    "c_after_hm": ("after paying off the short-term loan",
                   "богино хугацааны зээлээ төлсний дараа"),
    "c_after_hm_costs": ("after paying off the short-term loan and {x} in refinance costs",
                         "богино хугацааны зээл болон дахин санхүүжилтийн {x} зардлыг "
                         "төлсний дараа"),
    "note_brrr": ("After the refinance, your rent ÷ PITIA is {d}x and the new loan is {ltv} "
                  "of the value. {s}x or more and a loan of 80% or less: a lender is likely to "
                  "fund it. {m}x or more: a lender may fund it with extra conditions. "
                  "Under {m}x: a lender won't fund it.",
                  "Дахин санхүүжилтийн дараа таны түрээс / сарын төлбөрийн харьцаа {d}x, "
                  "шинэ зээл үнэлгээний {ltv}. Харьцаа {s}x буюу түүнээс дээш, зээл үнэлгээний "
                  "80 хувиас хэтрэхгүй бол банк зээл олгох магадлал өндөр. Харьцаа {m}x буюу "
                  "түүнээс дээш бол банк нэмэлт шаардлага тавьж зээл олгож болзошгүй. Харьцаа "
                  "{m}x хүрэхгүй бол банк зээл олгохгүй."),
    "l_hm_loan": ("Short-term loan", "Богино хугацааны зээл"),
    "c_pct_price": ("{x}% of the price", "үнийн {x}%"),
    "l_ltv_arv": ("Loan % of sale price", "Зээл, зарах үнийн %"),
    "c_cap75": ("lenders cap this at 75%", "зээлдүүлэгчид үүнийг 75%-иар хязгаарладаг"),
    "l_ltc": ("Loan % of total cost", "Зээл, нийт зардлын %"),
    "c_ltc": ("loan ÷ (price + repairs)", "зээл ÷ (үнэ + засвар)"),
    "l_time": ("Time to sell", "Зарах хугацаа"),
    "v_months": ("{n} months", "{n} сар"),
    "c_buy_sell": ("from buying to selling", "худалдаж авснаас зарах хүртэл"),
    "note_flip_ok": ("The loan is {x} of the sale price, under the 75% cap. "
                     "A short-term lender is likely to fund.",
                     "Зээл зарах үнийн дүнгийн {x}-ийг эзэлж байгаа нь зээлдүүлэгчийн 75%-ийн шалгуураас бага байна. "),
    "note_flip_bad": ("The loan is {x} of the sale price, over the 75% cap. "
                      "Expect the lender to lower the loan or say no.",
                      "Зээл зарах үнийн дүнгийн {x}-ийг эзэлж байгаа нь зээлдүүлэгчийн 75%-ийн шалгуураас их байна. "
                      "Зээлийн хэмжээг бууруулах эсвэл зээл олгохгүй байж болзошгүй."),
    "fund": ("Will a lender fund it?", "Банк зээл олгох уу?"),
    "a_STRONG": ("STRONG", "Шаардлагыг бүрэн хангасан"),
    "a_LIKELY": ("LIKELY", "Зээл олгох магадлал өндөр"),
    "a_CONDITIONAL": ("CONDITIONAL", "Нэмэлт шаардлагатайгаар олгож болзошгүй"),
    "a_LIKELY DECLINE": ("LIKELY DECLINE", "Зээл олгохгүй байх магадлал өндөр"),
    "a_DECLINE": ("DECLINE", "Зээл олгохгүй"),

    "a_MEETS MIN": ("MEETS THE LENDER'S MINIMUM", "Банкны доод шаардлагыг хангаж байна"),
    "a_LTV HIGH": ("LOAN TOO HIGH", "Зээлийн хэмжээ хэт өндөр"),
    "a_BELOW MIN": ("BELOW THE LENDER'S MINIMUM", "Банкны доод шаардлагыг хангахгүй байна"),
    "b_price": ("price", "үнийн"),
    "b_value": ("value after repairs", "засварын дараах үнэлгээний"),
    "after_refi": (" These figures are after the refinance.", " Энэ тооцоо дахин санхүүжилтийн дараах байдлаар."),
    "n_meets": ("Rent ÷ PITIA is {d}x and your lender's minimum is {m}x. The loan is {ltv} "
                "of the {base}, within the usual 80% limit. Rent could fall to {need} "
                "a month and still meet the minimum.",
                "Түрээс / сарын төлбөрийн харьцаа {d}x, банкны шаардах доод харьцаа {m}x. "
                "Зээл {base} {ltv} буюу ихэвчлэн тавигддаг 80 хувийн хязгаараас хэтрээгүй. "
                "Сарын түрээс {need} хүртэл буурсан ч банкны доод шаардлагыг хангана."),
    "n_ltv": ("Rent ÷ PITIA is {d}x, which meets your lender's minimum of {m}x, but the loan "
              "is {ltv} of the {base}. Most DSCR lenders lend up to 80%.",
              "Түрээс / сарын төлбөрийн харьцаа {d}x, банкны шаардах доод харьцаа {m}x тул "
              "хангаж байна. Гэвч зээл {base} {ltv} байна. Ихэнх банк 80 хувиас хэтрэхгүй "
              "зээл олгодог."),
    "n_below": ("Rent ÷ PITIA is {d}x and your lender's minimum is {m}x. Rent would need to "
                "be {need} a month to reach it.",
                "Түрээс / сарын төлбөрийн харьцаа {d}x, банкны шаардах доод харьцаа {m}x. "
                "Үүнд хүрэхийн тулд сарын түрээс {need} байх шаардлагатай."),
    # --- sensitivity ---
    "var_Purchase price": ("Purchase price", "Худалдан авах үнэ"),
    "var_Value after repairs": ("Value after repairs", "Засварын дараах үнэ цэнэ"),
    "var_Repair budget": ("Repair budget", "Засварын төсөв"),
    "var_Monthly rent": ("Monthly rent", "Сарын түрээс"),
    "var_New loan rate": ("New loan rate", "Шинэ зээлийн хүү"),
    "var_New loan % of value": ("New loan % of value", "Зээл, байрны үнэлгээний харьцаа"),
    "var_Home value growth": ("Home value growth", "Байрны үнийн өсөлт"),
    "var_Loan rate": ("Loan rate", "Зээлийн хүү"),
    "var_Empty months": ("Empty months", "Түрээслэгчгүй байх хугацаа"),
    "var_Rent increases": ("Rent increases", "Түрээсийн өсөлт"),
    "s_driver": ("**Biggest driver: {name}.** Within the changes tested below, your yearly "
                 "return ranges from **{lo}** to **{hi}** (your deal: {base}).",
                 "**Хамгийн их нөлөөлөх хүчин зүйл: {name}.** Доорх өөрчлөлтүүдийн хүрээнд "
                 "таны жилийн өгөөж **{lo}**-иас **{hi}** хүртэл байна (таны тооцоо: {base})."),
    "s_helps": ("Helps your return", "Өгөөжийг нэмэгдүүлнэ"),
    "s_hurts": ("Hurts your return", "Өгөөжийг бууруулна"),
    "s_lower": ("lower", "бага"),
    "s_higher": ("higher", "өндөр"),
    "s_hover": ("%{customdata[2]}: %{customdata[1]}<br>Yearly return: %{customdata[0]:.2%}<extra></extra>",
                "%{customdata[2]}: %{customdata[1]}<br>Жилийн өгөөж: %{customdata[0]:.2%}<extra></extra>"),
    "s_title": ("What moves your yearly return most<br><sup>Dotted line = your deal, {base}</sup>",
                "Жилийн өгөөжид юу хамгийн их нөлөөлөх вэ?<br><sup>Тасархай шугам = Таны хөрөнгө оруулалтын өгөөж, {base}</sup>"),
    "s_line": ("Your deal {base}", "Таны өгөөж {base}"),
    "s_flip_info": ("These charts are for rentals. A flip is judged on its profit, so check the "
                    "profit tests and Most you should offer in the Investor view.",
                    "Эдгээр график түрээсийн байранд зориулагдсан. Засаад зарах хөрөнгө оруулалтыг "
                    "ашгаар нь үнэлдэг тул Хөрөнгө оруулагчийн хувьд хэсгийн ашгийн шалгуур болон "
                    "санал болгох дээд үнийг харна уу."),
    "s_brrr_aco_info": ("This deal gives back all the cash you put in at the refinance, so there's "
                        "no yearly return to compare. Lower the value after repairs or the new "
                        "loan % to see this chart.",
                        "Дахин санхүүжилтээр оруулсан бүх мөнгөө буцааж авах тул харьцуулах жилийн "
                        "өгөөж байхгүй. Графикийг харахын тулд засварын дараах үнэ цэнэ эсвэл "
                        "зээл, байрны үнэлгээний харьцааг бууруулна уу."),
    "s_cap_brrr": ("Blue bars help your return, grey bars hurt it. Each bar changes one input up "
                   "or down, with everything else the same. Changes tested: value after repairs, "
                   "rent and price ±10%; repairs ±25%; new loan % ±5%; new loan rate ±1%.",
                   "Хэрхэн унших вэ: хэвтээ тэнхлэгт жилийн өгөөжийг, босоо тэнхлэгт өгөөжид "
                   "нөлөөлөх хүчин зүйлүүдийг харуулав. Багана бүр тухайн хүчин зүйлийн өсөлт, "
                   "бууралт нь хөрөнгө оруулалтын өгөөжид хэрхэн нөлөөлөхийг харуулна. Цэнхэр өнгөтэй "
                   "багана нь өгөөжид эерэгээр, саарал өнгөтэй багана нь сөргөөр нөлөөлөх өөрчлөлт. "
                   "Голд байгаа тасархай шугам нь таны оруулсан тоогоор гарсан хөрөнгө оруулалтын "
                   "өгөөж. Хүчин зүйл бүрийг дараах хэмжээгээр өсгөж, бууруулж тооцов: засварын дараах үнэ цэнэ, "
                   "түрээс ±10%; засварын төсөв ±25%; зээл, байрны үнэлгээний харьцаа ±5 нэгж хувь; шинэ зээлийн хүү ±1 нэгж хувь."),
    "s_aco_star": (" * At that change you'd get all your cash back at the refinance, so that bar "
                   "isn't comparable.",
                   " * Энэ өөрчлөлтөөр дахин санхүүжилтээр бүх мөнгөө буцааж авах тул тухайн "
                   "баганыг харьцуулах боломжгүй."),
    "s_cap_rental": ("Blue bars help your return, grey bars hurt it. Each bar changes one input up "
                     "or down, with everything else the same. Changes tested: price and rent ±10%; "
                     "loan rate and rent increases ±1%; empty months ±3%; home value growth ±1.5%.",
                     "Хэрхэн унших вэ: хэвтээ тэнхлэгт жилийн өгөөжийг, босоо тэнхлэгт өгөөжид "
                     "нөлөөлөх хүчин зүйлүүдийг харуулав. Багана бүр тухайн хүчин зүйлийн өсөлт, "
                     "бууралт нь хөрөнгө оруулалтын өгөөжид хэрхэн нөлөөлөхийг харуулна. Цэнхэр өнгөтэй "
                     "багана нь өгөөжид эерэгээр, саарал өнгөтэй багана нь сөргөөр нөлөөлөх өөрчлөлт. "
                     "Голд байгаа тасархай шугам нь таны оруулсан тоогоор гарсан хөрөнгө оруулалтын "
                     "өгөөж. Хүчин зүйл бүрийг дараах хэмжээгээр өсгөж, бууруулж тооцов: үнэ, түрээс "
                     "±10%; зээлийн хүү, түрээсийн өсөлт ±1 нэгж хувь; түрээслэгчгүй хугацаа ±3 нэгж "
                     "хувь; байрны үнийн өсөлт ±1.5 нэгж хувь."),
    "s_after_points": (" ({x}% after points)", " (оноо авсны дараа {x}%)"),
    "s_reach": ("**At your {rate} rate, you reach your {goal}% goal if you pay {price} or less.**",
                "**{rate} хүүтэй үед {price} буюу түүнээс бага төлбөл {goal}% зорилтдоо хүрнэ.**"),
    "s_no_price": ("**No price in this range reaches your {goal}% goal at this rate.**",
                   "**Энэ хүүгээр энэ хүрээний аль ч үнээр {goal}% зорилтод хүрэхгүй.**"),
    "s_heat_hover": ("Loan rate %{y}<br>Price %{x}<br>Yearly return %{z:.2%}<extra></extra>",
                     "Зээлийн хүү %{y}<br>Үнэ %{x}<br>Жилийн өгөөж %{z:.2%}<extra></extra>"),
    "s_return_short": ("Return", "Өгөөж"),
    "s_heat_title": ("Yearly return by price and loan rate (grey = your {goal}% goal)",
                     "Үнэ болон зээлийн хүүгээр жилийн өгөөж (саарал = таны {goal}% зорилт)"),
    "s_loan_rate": ("Loan rate", "Зээлийн хүү"),
    "s_heat_cap": ("How to read this: each cell is your yearly return if you paid that price "
                   "(across) at that loan rate (down). Blue beats your goal, red misses it. "
                   "The middle cell is your deal as entered.",
                   "Хэрхэн унших вэ: хэвтээ тэнхлэгт худалдан авах үнэ, "
                   "босоо тэнхлэгт зээлийн хүүг харуулав. Нүд бүрт худалдан авах үнэ болон "
                   "хүүгийн өөрчлөлтөөр гарах жилийн өгөөжийг харуулна. Цэнхэр өнгөтэй "
                   "нүдэнд өгөөж таны зорилтоос давсан, улаан өнгөтэй нүдэнд зорилтод хүрээгүй. "
                   "Голд байгаа нүд нь таны оруулсан үнэ, хүүгээр гарсан өгөөж."),

    # --- cash flow table ---
    "cf_amount": ("Amount", "Дүн"),
    "cf_price": ("Purchase price", "Худалдан авах үнэ"),
    "cf_repairs": ("Repairs", "Засвар"),
    "cf_hm_interest": ("Short-term loan interest", "Богино хугацааны зээлийн хүү"),
    "cf_hm_fee": ("Short-term lender fee", "Богино хугацааны зээлдүүлэгчийн шимтгэл"),
    "cf_closing": ("Buying closing costs", "Худалдан авахтай холбоотой зардал"),
    "cf_holding": ("Holding costs ({n} months)", "Эзэмших зардал ({n} сар)"),
    "cf_selling": ("Selling costs", "Борлуулалтын зардал"),
    "cf_total": ("Total cost", "Нийт зардал"),
    "cf_sale": ("Sale price", "Зарах үнэ"),
    "cf_cash_in": ("Cash you put in", "Оруулсан бэлэн мөнгө"),
    "cf_cap_flip": ("A flip is one buy and one sale, so this is a cost list rather than a yearly "
                    "table. Net profit = sale price minus total cost.",
                    "Засаад зарах нь нэг удаа авч, нэг удаа зарах тул жилийн хүснэгт биш, зардлын "
                    "жагсаалт байна. Цэвэр ашиг = зарах үнэ - нийт зардал."),
    "cf_year": ("Year {n}", "{n} {o} жил"),
    "cf_year_short": ("Y{n}", "{n} {o} жил"),
    "cf_gross_rent": ("Rent charged", "Түрээсийн орлого"),
    "cf_effective_income": ("Rent after empty months", "Түрээслэгчгүй хугацааны дараах түрээс"),
    "cf_operating_expenses": ("Running costs", "Үйл ажиллагааны зардал"),
    "cf_noi": ("Rent left after expenses", "Зардлын дараах түрээсийн орлого"),
    "cf_interest": ("Loan interest", "Хүүгийн төлбөр"),
    "cf_debt_service": ("Loan payments", "Зээлийн төлбөр"),
    "cf_capex_reserve": ("Saved for big repairs", "Засварт зориулсан нөөц"),
    "cf_cash_flow": ("Cash flow", "Мөнгөн гүйлгээ"),
    "cf_principal": ("Loan paid down (yours at sale)", "Төлөгдсөн үндсэн зээл (зарахад таных)"),
    "cf_cash_out_at_refi": ("Cash back at refinance", "Дахин санхүүжилтээр гаргаж авсан бэлэн мөнгө"),
    "cf_sale_proceeds": ("Cash from sale", "Борлуулалтаас орох мөнгө"),
    "cf_cap_brrr": ("Months 1 to {m}: the property is empty for repairs, so there is no rent. You "
                    "pay interest on the short-term loan plus property tax, insurance and HOA. After "
                    "the refinance, rent starts and the new 30-year loan's payments start. Cash flow "
                    "is rent left after expenses, minus loan payments and money saved for big repairs.",
                    "1-{m} {o} сар: засварын хугацаанд түрээслэгчгүй тул түрээсийн орлого байхгүй. "
                    "Богино хугацааны зээлийн хүү, үл хөдлөх эд хөрөнгийн албан татвар, даатгал, "
                    "СӨХ төлбөрийг төлнө. Дахин санхүүжилтийн дараа түрээс орж, шинэ 30 жилийн "
                    "зээлийн төлбөр эхэлнэ. Мөнгөн гүйлгээ = зардлын дараах түрээсийн орлого - "
                    "зээлийн төлбөр - засварт зориулсан нөөцийн зардал."),
    "cf_dscr_by_year": ("DSCR (rent ÷ PITIA), by year: {x}",
                        "Түрээс / сарын төлбөрийн харьцаа, жилээр: {x}"),
    "cf_cap_rental": ("Cash flow is rent left after expenses, minus the full loan payment "
                      "(interest and principal) and money saved for big repairs. The principal you "
                      "pay down comes back to you when you sell, as a smaller loan balance in the "
                      "cash from sale.",
                      "Мөнгөн гүйлгээ = зардлын дараах түрээсийн орлого - зээлийн төлбөр (хүү ба "
                      "үндсэн зээл) - засварт зориулсан нөөцийн зардал. Төлсөн үндсэн зээл тань "
                      "зарах үед зээлийн үлдэгдэл бага байх хэлбэрээр борлуулалтаас орох мөнгөнд "
                      "буцаж ирнэ."),

    # --- footer ---
    "disclaimer": ("For education and deal screening only. Not financial, lending, tax or "
                   "investment advice. Check every number with your own lender and advisors.",
                   "Зөвхөн сургалт болон анхан шатны үнэлгээнд зориулав. Санхүү, зээл, татвар, "
                   "хөрөнгө оруулалтын зөвлөгөө биш. Тоо бүрийг өөрийн зээлдүүлэгч, "
                   "зөвлөхүүдтэйгээ нягтална уу."),

}


def tr(lang):
    """Return a lookup function for the chosen language."""
    i = 0 if lang == "en" else 1

    def T(key, default=None, **kw):
        if key in TEXT:
            s = TEXT[key][i]
        else:
            s = key if default is None else default
        return s.format(**kw) if kw else s

    return T

def mn_ord(n):
    """Mongolian ordinal ending: 1 дэх, 2 дахь, 4 дэх, 9 дэх..."""
    n = int(n)
    d = n % 10
    if d:
        return "дэх" if d in (1, 4, 9) else "дахь"
    t = (n // 10) % 10
    if t:
        return "дэх" if t in (4, 9) else "дахь"
    return "дахь"