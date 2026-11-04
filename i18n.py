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
        "2. **Гэрээний мэдээллээ оруулна уу.** Тоо бичсний дараа Enter дарах, "
        "эсвэл − болон + товч ашиглана.\n"
        "3. **Шийдвэрийг уншина уу.** Дээрх талбарууд гол тоонуудыг харуулна; "
        "*Хөрөнгө оруулагчийн хувьд* шийдвэрийн шалтгаан болон юуг өөрчилбөл "
        "болохыг тайлбарлана; *Зээлдүүлэгчийн хувьд* банк зээлийг хэрхэн тооцож, "
        "олгох магадлалтайг харуулна.\n"
        "4. **Төлж болох дээд үнэ** нь зорилгоо хангасаар төлж болох хамгийн өндөр үнэ "
        "(Засаад зарах үед санал болгох дээд үнэ).",
    ),

    # --- dropdown options ---
    "st_Illinois": ("Illinois", "Иллинойс"),
    "st_California": ("California", "Калифорни"),
    "pt_SFH": ("SFH", "Хаус"),
    "pt_Condo": ("Condo", "Кондо (орон сууц)"),
    "pt_Townhouse": ("Townhouse", "Таунхаус"),
    "pt_Duplex": ("Duplex", "Хоёр айлын байшин"),
    "rt_Cash-Out": ("Cash-Out", "Бэлэн мөнгө авах"),
    "rt_Rate/Term": ("Rate/Term", "Хүү/хугацаа солих"),

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
                    "Бэлэн мөнгө авах: зээлийг бүтэн хувиар авч, бэлэн мөнгө буцааж авна. "
                    "Хүү/хугацаа солих: зөвхөн богино хугацааны зээлээ төлөх хэмжээгээр зээлнэ."),
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
    "t_cash_left": ("Cash left in deal", "Үлдсэн бэлэн мөнгө"),
    "t_margin": ("Profit as % of sale price", "Ашиг, зарах үнийн %"),
    "t_net_profit": ("Net profit", "Цэвэр ашиг"),
    "t_max_pay": ("Most you should pay", "Төлж болох дээд үнэ"),
    "c_goal": ("your goal {x}%", "таны зорилго {x}%"),
    "c_bank": ("bank wants 1.20x+", "банк 1.20x-ээс дээш шаарддаг"),
    "c_coc": ("of the cash you put in", "оруулсан бэлэн мөнгөнөөс"),
    "all_cash_out": ("All cash out", "Оруулсан мөнгөө бүрэн буцааж авсан"),
    "c_no_cash_left": ("no cash left in the deal", "хөрөнгө оруулалтаа бүрэн гаргаж авсан"),
    "c_refi_more": ("refi returns {x} more than invested",
                    "дахин санхүүжилт оруулснаас {x}-ээр их буцаана"),
    "c_of_invested": ("of {x} invested", "нийт {x} оруулснаас"),
    "c_flip_months": ("{n}-month flip, as a yearly rate", "{n} сарын засаад зарах, жилийн хувиар"),
    "c_holding": ("holding {x} / mo", "эзэмших зардал {x} / сар"),
    "c_vs_asking": ("vs {x} asking", "худалдагчийн зарах үнэ {x}"),
    "c_bank_sets": ("the bank test sets this · asking {x}",
                    "банкны шалгуураар тогтсон · худалдагчийн зарах үнэ {x}"),
    "c_goal_sets": ("your goal sets this · asking {x}",
                    "таны зорилгоор тогтсон · худалдагчийн зарах үнэ {x}"),
    "c_price_cant_fix": ("based on your goal; price can't fix the bank test",
                         "зорилгод үндэслэсэн; үнээр банкны шалгуурыг засах боломжгүй"),
    "na": ("n/a", "Хамаарахгүй"),
    "c_all_back": ("you get all your cash back at refi",
                   "дахин санхүүжилтээр бүх мөнгөө буцааж авна"),
    "none": ("none", "Байхгүй"),
    "c_no_price": ("no price meets the target", "зорилгод хүрэх үнэ алга"),

    # --- pop-ups ---
    "what_mean": ("What does this mean?", "Энэ юу гэсэн үг вэ?"),
    "p_return": (
        "**{irr} a year** is your average yearly return on the cash you put in.\n\n"
        "**After inflation: {real} a year.** Prices rise about {infl} a year, so future "
        "dollars buy less. This is what your return is worth in today's money.\n\n"
        "**Total profit over {years} years:** {profit}, or {real_profit} in today's dollars.",
        "**Жилд {irr}** нь таны оруулсан бэлэн мөнгөний дундаж жилийн өгөөж.\n\n"
        "**Инфляцийн дараа: жилд {real}.** Үнэ жилд ойролцоогоор {infl}-иар өсдөг тул "
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
        "Түрээслэгчгүй байх хугацаа болон зардлын дараа түрээсийн орлого {when} зээлийн төлбөрийг "
        "**{x} дахин** нөхөж байна. Банк дор хаяж **1.20x** шаарддаг тул түрээслэгч гарах "
        "эсвэл засвар гарах үед нөөц үлдэнэ. 1.00x-ээс доош бол зээлийн төлбөрийн нэг "
        "хэсгийг өөрийн мөнгөөр төлнө.",
    ),
    "p_coc_pos": (
        "In year 1 you keep **{x}** of the cash you put in, after the loan, expenses and "
        "money set aside for big repairs.",
        "Эхний жилд зээл, зардал болон томоохон засварын зардалын дараа оруулсан бэлэн "
        "мөнгөнийхөө **{x}**-ийг гартаа авна.",
    ),
    "p_coc_neg": (
        "In year 1 the rent doesn't cover everything: you add about **{x}** of the cash you "
        "put in, to pay the loan, expenses and money set aside for big repairs.",
        "Эхний жилд түрээс бүх зардлыг нөхөхгүй: зээл, зардал, томоохон засварын нөөцөд "
        "оруулсан бэлэн мөнгөнийхөө ойролцоогоор **{x}**-тэй тэнцэх мөнгийг нэмж төлнө.",
    ),
    "g_rental": ("hits your {x}% goal and passes the bank test",
                 "таны {x}% зорилгод хүрч, банкны шалгуурыг давах"),
    "g_brrr": ("still hits your {x}% goal", "таны {x}% зорилгод хүрэх"),
    "g_flip": ("still leaves your target profit after repairs, loan and selling costs",
               "засвар, зээл, борлуулалтын зардлын дараа зорилтот ашгаа хадгалах"),
    "p_max": ("**{price}** is the highest price that {goal}. Pay more and the numbers stop working.",
              "**{price}** бол {goal} хамгийн өндөр үнэ. Үүнээс илүү төлбөл тооцоо таарахгүй."),

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
        "Та зарахаасаа өмнө оноонд төлсөн мөнгөө сарын хэмнэлтээр буцааж олж амжихгүй. "
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
                  "Засварын зардалыг даах эсэх (банкных биш, таных): томоохон засварт мөнгө "
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