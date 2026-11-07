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
        "*Investor view* explains the verdict and what would fix it; "
        "*Lender view* shows how a lender sizes the loan and whether it is likely to fund.\n"
        "4. **Most you should pay** is the most you can pay and still meet your target "
        "(for Flip, the max allowable offer).",
        "1. **Хөрөнгө оруулалтын стратеги болон хувилбараа сонгоно уу** (дээд мөрөнд): "
        "Түрээсийн байр, АЗТД (Авах → Засах → Түрээслүүлэх → Дахин санхүүжүүлэх) "
        "эсвэл Засаад зарах; Гутранги, Суурь эсвэл Өөдрөг.\n"
        "2. **Үл хөдлөх эд хөрөнгийн мэдээллээ оруулна уу.** Мэдээлэлээ бичсэний дараа Enter дарах, "
        "эсвэл − болон + товч ашиглана.\n"
        "3. **Шийдвэрийг уншина уу.** Танд санхүүгийн үзүүлэлтүүдийг харуулна; "
        "*Хөрөнгө оруулагчийн хувьд* шийдвэрийн шалтгаан болон мөн ямар хүчин зүйлийг өөрчилбөл "
        "та хөрөнгө оруулалтын зорилгодоо хүрэхийг тайлбарлана; *Зээлдүүлэгчийн хувьд* банк зээлийг хэрхэн тооцож, "
        "зээл олгох магадлалыг харуулна.\n"
        "4. **Төлж болох дээд үнэ** нь таны хүсэж байгаа хөрөнгө оруулалтын өгөөжийн зорилгыг хангах дээд үнэ "
        "(Засаад зарах үед: засвар, зээл, эзэмших болон борлуулалтын зардлын дараа ашгийн зорилгодоо хүрэхийн тулд худалдагчид санал болгох хамгийн өндөр үнэ).",
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
    "points": ("Points to lower rate", "Хүү бууруулах оноо (points)"),

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
    "h_hm_ltv": ("The short-term (hard money) loan as a % of the price.",
                 "Богино хугацааны (hard money) зээл, үнийн хувиар."),
    "h_hm_rate": ("Yearly interest on the short-term loan. You pay interest only.",
                  "Богино хугацааны зээлийн жилийн хүү. Зөвхөн хүүг нь төлнө."),
    "h_refi_month": ("When you swap the short-term loan for a regular 30-year loan.",
                     "Богино хугацааны зээлийг ердийн 30 жилийн зээлээр солих хугацаа."),
    "h_refi_ltv": ("The new 30-year loan as a % of the value after repairs.",
                   "Шинэ 30 жилийн зээлийн дүнг засварын дараах үнэлгээнд харьцуулсан хувь (ЗҮХ)."),
    "h_post_rate": ("Yearly interest rate on the new 30-year loan.",
                    "Шинэ 30 жилийн зээлийн жилийн хүү."),
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
    "h_hoa": ("Leave blank to use the state and property-type default.",
              "Хоосон орхивол муж болон байрны төрлийн үндсэн дүнг ашиглана."),
    "h_points": ("Each point costs 1% of the loan (for BRRR, the new loan) "
                 "and lowers your rate by about 0.25%.",
                 "Нэг оноо зээлийн 1%-тай тэнцэх үнэтэй (BRRR-д шинэ зээлийн) "
                 "бөгөөд хүүг ойролцоогоор 0.25%-иар бууруулна."),

        # --- verdict + tiles ---
    "verdict": ("Verdict", "Шийдвэр"),
    "v_HARD REJECT": ("HARD REJECT", "Шууд татгалзах"),
    "v_REJECT": ("REJECT", "Татгалзах"),
    "v_NEGOTIATE": ("NEGOTIATE", "Нөхцөл тохиролцох"),
    "v_ACCEPT": ("ACCEPT", "Худалдан авах"),
    "v_BUY": ("BUY", "Худалдан авах"),
    "t_return": ("Yearly return", "Жилийн өгөөж"),
    "t_dscr": ("Rent covers loan", "Түрээс / зээлийн төлбөрийн харьцаа"),
    "t_coc": ("First-year cash return", "Эхний жилийн бэлэн мөнгөний өгөөж"),
    "t_cash_left": ("Your money still in the property", "Үлдэгдэл хөрөнгө оруулалт"),
    "t_margin": ("Profit as % of sale price", "Ашиг, зарах үнийн %"),
    "t_net_profit": ("Net profit", "Цэвэр ашиг"),
    "t_max_pay": ("Most you should pay", "Төлж болох дээд үнэ"),
    "c_goal": ("your goal {x}%", "таны зорилт {x}%"),
    "c_bank": ("bank wants 1.20x+", "банк 1.20x-ээс дээш шаарддаг"),
    "c_coc": ("of the cash you put in", "оруулсан бэлэн мөнгөнөөс"),
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
    "when_rental": ("in the worst year", "хамгийн муу жилд"),
    "when_brrr": ("after the refi", "дахин санхүүжилтийн дараа"),
    "p_dscr": (
        "After vacancy and expenses, the rent covers your loan payment **{x} times** {when}. "
        "Banks want at least **1.20x**, so there's a cushion if a tenant leaves or a repair "
        "comes up. Below 1.00x, you pay part of the loan from your own pocket.",
        "Холбогдох зардлыг хассаны дараах түрээсийн орлого {when} зээлийн төлбөрийн **{pct}**-ийг "
        "төлөхөд хүрч байна. Банк дор хаяж **120%** (1.20x) шаарддаг. 100%-иас бага бол "
        "зээлийн төлбөрийн дутуу хэсгийг өөрийн мөнгөөр төлнө.",
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
                 "таны {x}% зорилгод хүрч, банкны шалгуурыг давах"),
    "g_brrr": ("still hits your {x}% goal", "таны {x}% зорилгод хүрэх"),
    "g_flip": ("still leaves your target profit after repairs, loan and selling costs",
               "засвар, зээл, борлуулалтын зардлын дараа зорилтот ашгаа хадгалах"),
    "p_max": ("**{price}** is the highest price that {goal}. Pay more and the numbers stop working.",
              "**{price}** бол {goal} хамгийн өндөр үнэ. Үүнээс илүү төлбөл тооцоо таарахгүй."),
    "pm_goal": ("The seller is asking **{asking}**. Don't pay more than **{price}**: above that, "
                "your yearly return falls below your **{goal}%** goal.",
                "Худалдагчийн зарах үнэ **{asking}**. Та **{price}**-аас илүү төлөх ёсгүй: "
                "үүнээс их төлбөл жилийн өгөөж таны **{goal}%** зорилгод хүрэхгүй."),
    "pm_bank": ("The seller is asking **{asking}**. Don't pay more than **{price}**: above that, "
                "the loan gets too big and fails the bank test (rent must cover the loan 1.20x).",
                "Худалдагчийн зарах үнэ **{asking}**. Та **{price}**-аас илүү төлөх ёсгүй: "
                "үүнээс их төлбөл зээл томорч, банкны шалгуурыг (түрээс / зээлийн төлбөрийн "
                "харьцаа 1.20x) давахгүй."),
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
                      "Ашгийн зорилго: зарах үнийн {x}. Таны зорилго {goal}%."),
    "k_bank": ("Bank test: rent covers the loan {x}x. The bank wants 1.20x.",
               "Банкны шалгуур: түрээсийн төлбөр болон зээлийн төлбөрийн харьцаа {x}x. "
               "Банк 1.20x шаарддаг."),
    "k_return_aco": ("Return test: the refi gives back all the cash you put in",
                    "Өгөөж зорилгод хүрсэн эсэх: дахин санхүүжилтээр оруулсан бүх мөнгөө буцааж авна"),
    "k_return": ("Return test: {x} a year. Your goal is {goal}%.",
                "Өгөөж зорилгод хүрсэн эсэх: жилд {x}. Таны зорилго {goal}%."),
    "k_repairs": ("Repairs test (yours, not the bank's): after saving for big repairs, "
                  "rent covers the loan {x}x",
                  "Засварын зардлыг даах эсэх (банкных биш, таных): томоохон засварт мөнгө "
                  "хуримтлуулсны дараа түрээс зээлийг {x}x нөхөнө"),
    "k_repairs_low": (". Below 1.00x, you'd add your own money for big repairs.",
                      ". 1.00x-ээс доош бол томоохон засварт өөрийн мөнгө нэмнэ."),
    "f_mao_below": ("Most you should offer: **{mao}**, {x} below the asking price",
                    "Санал болгох дээд үнэ: **{mao}**, худалдагчийн зарах үнээс {x}-ээр бага"),
    "f_mao_under": ("Most you should offer: **{mao}**. The asking price is already {x} under it",
                    "Санал болгох дээд үнэ: **{mao}**. Худалдагчийн үнэ үүнээс {x}-ээр аль хэдийн бага"),
    "f_rent_bank": ("Rent the bank needs to see: **{x}**", "Банкны шаардах түрээс: **{x}**"),
    "f_rent_repairs": ("Rent to also cover big repairs: **{x}**",
                       "Томоохон засварыг давхар нөхөх түрээс: **{x}**"),
    "f_max_goal": ("Most you can pay to hit your {goal}% goal: **{x}**",
                   "{goal}% зорилгод хүрэх дээд үнэ: **{x}**"),
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
    "c_bank_strong": ("bank wants 1.20x, 1.25x for strong",
                      "банк 1.20x шаарддаг, 1.25x бол сайн"),
    "note_rental": ("Rent covers the loan {d}x and the loan is {ltv} of the price. "
                    "Strong needs 1.25x and 80% or less; conditional needs 1.20x.",
                    "Түрээсийн төлбөр болон зээлийн төлбөрийн харьцаа {d}x, зээл үнийн {ltv}. "
                    "Сайн үнэлгээнд 1.25x ба 80%-иас бага; нөхцөлтэйд 1.20x шаардлагатай."),
    "l_cap": ("Cap rate", "Капиталжуулалтын түвшин"),
    "c_cap": ("rent left after expenses ÷ price", "зардлын дараах түрээсийн орлого ÷ үнэ"),
    "p_cap": (
        "If you paid **all cash** with no loan, you'd earn **{x}** a year from rent: "
        "{noi} left after expenses ÷ {price} price.\n\n"
        "It ignores the loan, so you can compare properties side by side. Compare it with "
        "similar rentals in the same area: higher means more income for the price.",
        "Зээлгүйгээр **бүхэлд нь бэлнээр** төлсөн бол түрээсээс жилд **{x}** олно: "
        "зардлын дараах {noi} ÷ {price} үнэ.\n\n"
        "Зээлийг тооцдоггүй тул үл хөдлөх хөрөнгүүдийг хооронд нь харьцуулж болно. "
        "Ижил бүсийн түрээсийн байртай харьцуулаарай: өндөр байх тусам үнэдээ илүү орлоготой.",
    ),
    "l_new_loan": ("New loan", "Шинэ зээл"),
    "c_on_arv": ("on a value after repairs of {x}", "засварын дараах {x} үнэ цэнэд"),
    "l_refi_ltv": ("New loan % of value", "Зээл, байрны үнэлгээний харьцаа"),
    "c_refi_at": ("{type}, refinance at month {m}", "{type}, {m} {o} сард"),
    "l_cash_back": ("Cash back at refinance", "Дахин санхүүжилтээр авах бэлэн мөнгө"),
    "c_after_hm": ("after paying off the short-term loan",
                   "богино хугацааны зээлээ төлсний дараа"),
    "note_brrr": ("After the refinance, rent covers the loan {d}x and the new loan is {ltv} "
                  "of the value. Strong needs 1.25x and 80% or less; conditional needs 1.20x.",
                  "Дахин санхүүжилтийн дараа түрээсийн төлбөр болон зээлийн төлбөрийн харьцаа {d}x, "
                  "шинэ зээл үнэлгээний {ltv}. Сайн үнэлгээнд 1.25x ба 80%-иас бага; "
                  "нөхцөлтэйд 1.20x шаардлагатай."),
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
                     "Зээл зарах үнийн {x}, 75%-ийн хязгаараас бага. "
                     "Богино хугацааны зээлдүүлэгч санхүүжүүлэх магадлалтай."),
    "note_flip_bad": ("The loan is {x} of the sale price, over the 75% cap. "
                      "Expect the lender to lower the loan or say no.",
                      "Зээл зарах үнийн {x}, 75%-ийн хязгаараас их. "
                      "Зээлдүүлэгч зээлийг бууруулах эсвэл татгалзаж болзошгүй."),
    "fund": ("Will a lender fund it?", "Зээлдүүлэгч санхүүжүүлэх үү?"),
    "a_STRONG": ("STRONG", "Сайн"),
    "a_LIKELY": ("LIKELY", "Магадлалтай"),
    "a_CONDITIONAL": ("CONDITIONAL", "Нөхцөлтэй"),
    "a_LIKELY DECLINE": ("LIKELY DECLINE", "Татгалзах магадлалтай"),
    "a_DECLINE": ("DECLINE", "Татгалзана"),

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
                 "таны жилийн өгөөж **{lo}**-аас **{hi}** хооронд байна (таны тооцоо: {base})."),
    "s_helps": ("Helps your return", "Өгөөжийг нэмэгдүүлнэ"),
    "s_hurts": ("Hurts your return", "Өгөөжийг бууруулна"),
    "s_lower": ("lower", "бага"),
    "s_higher": ("higher", "өндөр"),
    "s_hover": ("If %{y} is %{customdata[1]}: yearly return %{customdata[0]:.2%}<extra></extra>",
                "%{y} %{customdata[1]} бол: жилийн өгөөж %{customdata[0]:.2%}<extra></extra>"),
    "s_title": ("What moves your yearly return most<br><sup>Dotted line = your deal, {base}</sup>",
                "Жилийн өгөөжид юу хамгийн их нөлөөлөх вэ<br><sup>Тасархай шугам = таны тооцоо, {base}</sup>"),
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
                   "Цэнхэр нь өгөөжийг нэмэгдүүлж, саарал нь бууруулна. Бусдыг нь хэвээр үлдээж, "
                   "нэг үзүүлэлтийг өсгөж эсвэл бууруулсан. Шалгасан өөрчлөлт: засварын дараах "
                   "үнэ цэнэ, түрээс, үнэ ±10%; засвар ±25%; зээлийн харьцаа ±5%; шинэ зээлийн хүү ±1%."),
    "s_aco_star": (" * At that change you'd get all your cash back at the refinance, so that bar "
                   "isn't comparable.",
                   " * Энэ өөрчлөлтөөр дахин санхүүжилтээр бүх мөнгөө буцааж авах тул тухайн "
                   "баганыг харьцуулах боломжгүй."),
    "s_cap_rental": ("Blue bars help your return, grey bars hurt it. Each bar changes one input up "
                     "or down, with everything else the same. Changes tested: price and rent ±10%; "
                     "loan rate and rent increases ±1%; empty months ±3%; home value growth ±1.5%.",
                     "Цэнхэр нь өгөөжийг нэмэгдүүлж, саарал нь бууруулна. Бусдыг нь хэвээр үлдээж, "
                     "нэг үзүүлэлтийг өсгөж эсвэл бууруулсан. Шалгасан өөрчлөлт: үнэ, түрээс ±10%; "
                     "зээлийн хүү, түрээсийн өсөлт ±1%; түрээслэгчгүй хугацаа ±3%; байрны үнийн өсөлт ±1.5%."),
    "s_after_points": (" ({x}% after points)", " (оноо авсны дараа {x}%)"),
    "s_reach": ("**At your {rate} rate, you reach your {goal}% goal if you pay {price} or less.**",
                "**{rate} хүүтэй үед {price} буюу түүнээс бага төлбөл {goal}% зорилгодоо хүрнэ.**"),
    "s_no_price": ("**No price in this range reaches your {goal}% goal at this rate.**",
                   "**Энэ хүүгээр энэ хүрээний аль ч үнээр {goal}% зорилгод хүрэхгүй.**"),
    "s_heat_hover": ("Loan rate %{y}<br>Price %{x}<br>Yearly return %{z:.2%}<extra></extra>",
                     "Зээлийн хүү %{y}<br>Үнэ %{x}<br>Жилийн өгөөж %{z:.2%}<extra></extra>"),
    "s_return_short": ("Return", "Өгөөж"),
    "s_heat_title": ("Yearly return by price and loan rate (grey = your {goal}% goal)",
                     "Үнэ болон зээлийн хүүгээр жилийн өгөөж (саарал = таны {goal}% зорилго)"),
    "s_loan_rate": ("Loan rate", "Зээлийн хүү"),
    "s_heat_cap": ("How to read this: each cell is your yearly return if you paid that price "
                   "(across) at that loan rate (down). Blue beats your goal, red misses it. "
                   "The middle cell is your deal as entered.",
                   "Хэрхэн унших вэ: нүд бүр тухайн үнээр (хэвтээ) болон зээлийн хүүгээр (босоо) "
                   "авбал гарах жилийн өгөөжийг харуулна. Цэнхэр нь зорилгоос давсан, улаан нь "
                   "хүрээгүй. Голын нүд нь таны оруулсан тооцоо."),

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
                    "жагсаалт байна. Цэвэр ашиг = зарах үнэ хасах нийт зардал."),
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
    "cf_cap_brrr": ("Months 1 to {m}: you pay only interest on the short-term loan. After that, the "
                    "new 30-year loan's payments start. Cash flow is rent left after expenses, minus "
                    "loan payments and money saved for big repairs.",
                    "1-{m} {o} сар: богино хугацааны зээлийн зөвхөн хүүг төлнө. Үүний дараа шинэ "
                    "30 жилийн зээлийн төлбөр эхэлнэ. Мөнгөн гүйлгээ = зардлын дараах түрээсийн "
                    "орлого - зээлийн төлбөр - засварт зориулсан нөөцийн зардал."),
    "cf_dscr_by_year": ("Rent covers loan, by year: {x}",
                        "Түрээсийн төлбөр болон зээлийн төлбөрийн харьцаа, жилээр: {x}"),
    "cf_cap_rental": ("Cash flow is rent left after expenses, minus loan interest and money saved for "
                      "big repairs. The loan you pay down is shown separately, because you get it "
                      "back when you sell.",
                      "Мөнгөн гүйлгээ = зардлын дараах түрээсийн орлого - хүүгийн төлбөр - "
                      "засварт зориулсан нөөцийн зардал. Төлөгдсөн үндсэн зээлийг тусад нь харуулсан, учир нь "
                      "зарах үед үүнийг буцааж авна."),

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