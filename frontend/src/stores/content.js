import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { api } from "@/lib/api";

const STORAGE_KEY = "navar_content_v1";

function defaultContent() {
  return {
    home: {
      heroTag: "مجموعه ۱۴۰۳",
      heroTitle: "قهوه‌ای که\nمی‌خواستی.",
      heroSubtitle:
        "ما دانه‌های تک‌خاستگاه را از مزارع شناخته‌شده تهیه می‌کنیم و در کارگاه کوچک خود تازه برشته می‌کنیم.",
      heroCtaPrimary: "مشاهده محصولات",
      heroCtaSecondary: "داستان ما",
      featuredTag: "منتخب",
      featuredTitle: "بهترین‌های این فصل",
      featuredSubtitle:
        "هر فنجان روایت یک سفر است — از مزرعه تا فنجان شما.",
    },
    about: {
      heroTag: "درباره ما",
      heroTitle: "قهوه را همان‌طور که هست، دوست داریم.",
      storyTitle: "داستان ما",
      storyParagraphs: [
        "نوار سال ۱۴۰۰ در یک کارگاه کوچک متولد شد. باوری ساده داشتیم: قهوه‌ی خوب نباید پیچیده باشد. باید تازه، شفاف و قابل ردیابی باشد.",
        "ما با کشاورزانی همکاری می‌کنیم که با عشق به خاکشان کار می‌کنند، و در کارگاه خودمان دانه‌ها را در دفعات کوچک برشته می‌کنیم تا هر فنجان دقیق‌ترین نسخه‌ی خودش باشد.",
        "امروز هزاران فنجان از نوار در سراسر ایران دم می‌شود — و این تازه آغاز است.",
      ],
      stats: [
        { value: "۲۰۰+", label: "مشتری دائمی" },
        { value: "۱۲", label: "خاستگاه فعال" },
        { value: "۴۸ ساعت", label: "تازگی تضمینی" },
      ],
      timeline: [
        {
          year: "۱۴۰۰",
          title: "آغاز ماجرا",
          description:
            "نوار در یک کارگاه کوچک در تهران با یک رستر ۵ کیلویی و باور به شفافیت زنجیره‌ی قهوه شروع کرد.",
        },
        {
          year: "۱۴۰۱",
          title: "اولین خاستگاه‌ها",
          description:
            "قراردادهای مستقیم با ۳ مزرعه از اتیوپی و کلمبیا — اول در ایران که قهوه‌ی تک‌خاستگاه با منشأ مشخص عرضه می‌کرد.",
        },
        {
          year: "۱۴۰۲",
          title: "گسترش کارگاه",
          description:
            "رستر جدید با ظرفیت ۱۵ کیلو، تیم ۶ نفره، و راه‌اندازی فروشگاه آنلاین با ارسال به سراسر ایران.",
        },
        {
          year: "۱۴۰۳",
          title: "نوار امروز",
          description:
            "بیش از ۲۰۰ مشتری دائمی، ۱۲ خاستگاه فعال، و تضمین تازگی ۴۸ ساعته از لحظه‌ی برشتن تا درِ خانه‌ی شما.",
        },
      ],
      mission:
        "ماموریت ما ساده است: قهوه‌ای باکیفیت، شفاف و قابل ردیابی به دست هر کسی که ارزش یک فنجان خوب را می‌داند برسانیم.",
      vision:
        "ایران را در نقشه‌ی دنیای قهوه‌ی اسپشیالتی قرار دهیم — نه به‌عنوان مصرف‌کننده، بلکه به‌عنوان بازیگری آگاه و با ذوق.",
      values: [
        {
          title: "شفافیت",
          description:
            "از مزرعه تا فنجان، همه چیز قابل ردیابی است. ما پنهان نمی‌کنیم.",
        },
        {
          title: "کیفیت بی‌تعارف",
          description:
            "هیچ دسته‌ای از دانه بدون تأیید تیم ما رست نمی‌شود.",
        },
        {
          title: "احترام به کشاورز",
          description:
            "قیمت عادلانه، رابطه‌ی بلندمدت، و دیده‌شدن کسانی که قهوه را می‌رویانند.",
        },
        {
          title: "تازگی همیشه",
          description:
            "رست در دفعات کوچک، ارسال سریع، تضمین ۴۸ ساعته.",
        },
      ],
    },
    contact: {
      heroTag: "تماس با ما",
      heroTitle: "همیشه پاسخگوییم.",
      address: "تهران، خیابان ولیعصر، کوچه بهار، پلاک ۱۲",
      phone: "۰۲۱-۸۸۱۲۳۴۵۶",
      email: "hello@navar.coffee",
      workingHours: "شنبه تا پنجشنبه، ۹ صبح تا ۶ عصر",
      mapLat: 35.7219,
      mapLng: 51.3347,
    },
  };
}

function deepMerge(target, source) {
  const out = { ...target };
  for (const key of Object.keys(source)) {
    if (
      source[key] &&
      typeof source[key] === "object" &&
      !Array.isArray(source[key]) &&
      target[key] &&
      typeof target[key] === "object" &&
      !Array.isArray(target[key])
    ) {
      out[key] = deepMerge(target[key], source[key]);
    } else {
      out[key] = source[key];
    }
  }
  return out;
}

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export const useContentStore = defineStore("content", () => {
  const defaults = defaultContent();
  const saved = loadFromStorage();
  const initial = saved ? deepMerge(defaults, saved) : defaults;

  const content = ref(initial);
  const loading = ref(false);

  async function fetchContent() {
    loading.value = true;
    try {
      const data = await api.content.get();
      const merged = deepMerge(defaultContent(), data);
      content.value = merged;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
    } catch {
      const cached = loadFromStorage();
      if (cached) content.value = deepMerge(defaults, cached);
    }
    loading.value = false;
  }

  async function saveToServer() {
    try {
      await api.admin.content.update({
        home: content.value.home,
        about: content.value.about,
        contact: content.value.contact,
      });
    } catch {
      // silent
    }
  }

  watch(
    content,
    (val) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(val));
      saveToServer();
    },
    { deep: true }
  );

  function update(path, value) {
    const keys = path.split(".");
    let obj = content.value;
    for (let i = 0; i < keys.length - 1; i++) {
      obj = obj[keys[i]];
    }
    obj[keys[keys.length - 1]] = value;
  }

  function reset() {
    content.value = defaultContent();
  }

  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(content.value));
    saveToServer();
  }

  fetchContent();

  return { content, loading, update, save, reset };
});
