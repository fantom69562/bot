import json


def xotira(matn):
    with open("jurnal.txt", "a", encoding="utf-8") as f:
        f.write(matn + "\n")


class Mehmon:
    def init(self, ism, tel):
        self.ism = ism
        self.tel = tel


class Xona:
    def init(self, raqam, narx, sigim=2):
        self.raqam = raqam
        self.narx = narx
        self.sigim = sigim
        self.mehmon = None
        self.lyuks = False

    def band_qil(self, mehmon):
        self.mehmon = mehmon

    def boshat(self):
        self.mehmon = None

    def repr(self):
        holat = f"Band ({self.mehmon.ism})" if self.mehmon else "Bo'sh"
        return f"Xona {self.raqam} | Narxi: {self.narx} so'm | {holat}"


class Lyuks(Xona):
    def init(self, raqam, narx, sigim=4):
        super().init(raqam, narx, sigim)
        self.lyuks = True

    def repr(self):
        holat = f"Band ({self.mehmon.ism})" if self.mehmon else "Bo'sh"
        return f"💎 Lyuks Xona {self.raqam} | Narxi: {self.narx} so'm | {holat}"


class Mehmonxona:
    def init(self, nom):
        self.nom = nom
        self.xonalar = []

    def xona_qosh(self, xona):
        self.xonalar.append(xona)

    def top(self, raqam):
        for x in self.xonalar:
            if x.raqam == raqam:
                return x
        return None

    def hammasi(self):
        if not self.xonalar:
            print("Xonalar mavjud emas.")
            return
        for x in self.xonalar:
            print(" ", x)

    def joylash(self, raqam, mehmon):
        x = self.top(raqam)
        if x:
            if x.mehmon:
                print("❌ Bu xona allaqachon band!")
            else:
                x.band_qil(mehmon)
                xotira(f"Xona {raqam} ga {mehmon.ism} joylashdi")
                print(f"✅ {mehmon.ism} {raqam}-xonaga joylashtirildi")
        else:
            print("❌ Bunday xona topilmadi")

    def boshat(self, raqam):
        x = self.top(raqam)
        if x and x.mehmon:
            ism = x.mehmon.ism
            x.boshat()
            xotira(f"Xona {raqam} bo'shatildi ({ism})")
            print(f"🟢 Xona {raqam} bo'shatildi")
        else:
            print("❌ Xona topilmadi yoki u allaqachon bo'sh")

    def boshlar(self):
        return [x for x in self.xonalar if x.mehmon is None]

    def eng_qimmat(self):
        if not self.xonalar:
            return None
        return max(self.xonalar, key=lambda x: x.narx)

    def daromad(self):
        return sum(x.narx for x in self.xonalar if x.mehmon is not None)

    def saqla(self, fayl="mehmonxona.json"):
        data = []
        for x in self.xonalar:
            mehmon_info = [x.mehmon.ism, x.mehmon.tel] if x.mehmon else None
            data.append(
                {
                    "raqam": x.raqam,
                    "narx": x.narx,
                    "sigim": x.sigim,
                    "lyuks": x.lyuks,
                    "mehmon": mehmon_info,
                }
            )
        with open(fayl, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("💾 Ma'lumotlar saqlandi!")

    @classmethod
    def yukla(cls, nom, fayl="mehmonxona.json"):
        m = cls(nom)
        try:
            with open(fayl, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("ℹ️ Saqlangan fayl topilmadi — bo'sh mehmonxona ochildi")
            return m
        for d in data:
            if d["lyuks"]:
                x = Lyuks(d["raqam"], d["narx"], d["sigim"])
            else:
                x = Xona(d["raqam"], d["narx"], d["sigim"])
            if d["mehmon"]:
                x.band_qil(Mehmon(*d["mehmon"]))
            m.xona_qosh(x)
        print(f"📂 {len(m.xonalar)} ta xona yuklandi")
        xotira(f"{len(m.xonalar)} ta xona fayldan yuklandi")
        return m

    def len(self):
        return len(self.xonalar)

    def add_room(m):
        raqam = int(input("Xona raqami: "))
        if m.top(raqam):
            print("❌ Bu raqamli xona bor!")
            return
        narx = int(input("Narxi: "))
        turi = input("Turi (oddiy/lyuks): ").strip().lower()
        if turi == "lyuks":
            m.xona_qosh(Lyuks(raqam, narx))
        else:
            m.xona_qosh(Xona(raqam, narx))

    def all_rooms(m):
        m.hammasi()

    def assign_guest(m):
        raqam = int(input("Xona raqami: "))
        ism = input("Mehmon ismi: ")
        tel = input("Telefon: ")
        m.joylash(raqam, Mehmon(ism, tel))

    def release_room(m):
        m.boshat(int(input("Xona raqami: ")))

    def show_rooms(m):
        bosh = m.boshlar()
        print(f"🟢 Bo'sh xonalar: {len(bosh)} ta")
        for x in bosh:
            print("  ", x)

    def show_expensive_room(m):
        x = m.eng_qimmat()
        print("💎", x if x else "Xonalar yo'q")

    def show_daily_income(m):
        print(f"💰 Bugungi daromad: {m.daromad()} so'm")

    def save_hotel(m):
        m.saqla()

    def show_journal():
        try:
            with open("jurnal.txt", "r", encoding="utf-8") as f:
                print(.read().strip() or "(jurnal bo'sh)")
                except FileNotFoundError:
                print("(jurnal hali yaratilmagan)")

        def exit_hotel(m):
            m.saqla()
            print("👋 Xayr Uyinga bor endi!")
            return True

        def main():
            print("""
    === 🏨 MEHMONXONA ===
    1. Xona qo'shish
    2. Barcha xonalar
    3. Mehmon joylash
    4. Xonani bo'shatish
    5. Bo'sh xonalar
    6. Eng qimmat xona
    7. Bugungi daromad
    8. Saqlash
    9. Jurnalni ko'rish
    0. Chiqish""")

            m = Mehmonxona.yukla("Hamroh Hotel")
            while True:
                choise = input("Tanlang: ")
                try:
                    if choise == "1":
                        add_room(m)
                    elif choise == "2":
                        all_rooms(m)
                    elif choise == "3":
                        assign_guest(m)
                    elif choise == "4":
                        release_room(m)
                    elif choise == "5":
                        show_rooms(m)
                    elif choise == "6":
                        show_expensive_room(m)
                    elif choise == "7":
                        show_daily_income(m)
                    elif choise == "8":
                        save_hotel(m)
                    elif choise == "9":
                        show_journal()
                    elif choise == "0":
                        if exit_hotel(m):
                            break
                    else:
                        print("❌ Noto'g'ri tanlov")
                except ValueError:
                    print("❌ Son kirit nima kiritmoqchi bovosan?")
                finally:
                    print(f"Jami xonalarimiz soni: {len(m)}")

        if name == "main":
            main()
            `