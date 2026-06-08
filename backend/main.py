from __future__ import annotations

import os
import json
import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Float, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
import hashlib
import hmac
import jwt as pyjwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

# ─── Config ──────────────────────────────────────────────────────────────────
DATABASE_URL = "sqlite:///./coffeeyar.db"
SECRET_KEY = os.environ.get("SECRET_KEY", "coffeeyar-secret-key-change-in-prod-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
security = HTTPBearer(auto_error=False)

# ─── DB Models ───────────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, default="")
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    wishlist = relationship("Wishlist", back_populates="user", cascade="all, delete")
    reviews = relationship("Review", back_populates="user")
    orders = relationship("Order", back_populates="user")
    addresses = relationship("Address", back_populates="user", cascade="all, delete")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    icon = Column(String, default="📦")
    color = Column(String, default="#6b7280")
    image = Column(String, default="")
    description = Column(Text, default="")
    display_order = Column(Integer, default=0)
    has_variants = Column(Boolean, default=False)
    variant_label = Column(String, default="")
    has_grinds = Column(Boolean, default=False)
    default_variants_json = Column(Text, default="[]")
    default_grinds_json = Column(Text, default="[]")
    attributes_json = Column(Text, default="[]")
    is_active = Column(Boolean, default=True)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    short_description = Column(String, default="")
    description = Column(Text, default="")
    price_toman = Column(Integer, default=0)
    discount_toman = Column(Integer, default=0)
    stock_qty = Column(Integer, default=0)
    has_variants = Column(Boolean, default=False)
    image = Column(String, default="")
    gallery_json = Column(Text, default="[]")
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    sku = Column(String, default="")
    seo_title = Column(String, default="")
    seo_description = Column(String, default="")
    specs_json = Column(Text, default="[]")
    notes_json = Column(Text, default="[]")
    flavor_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)
    category = relationship("Category", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete")
    reviews = relationship("Review", back_populates="product")
    faqs = relationship("ProductFaq", back_populates="product", cascade="all, delete")

class ProductVariant(Base):
    __tablename__ = "product_variants"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    title = Column(String, nullable=False)
    sku = Column(String, default="")
    image = Column(String, default="")
    price_toman = Column(Integer, default=0)
    discount_toman = Column(Integer, default=0)
    stock_qty = Column(Integer, default=0)
    display_order = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    attributes_json = Column(Text, default="{}")
    product = relationship("Product", back_populates="variants")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    ref = Column(String, unique=True, index=True, default=lambda: "NV-" + secrets.token_hex(3).upper())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    shipping_address = Column(Text, default="")
    notes = Column(Text, default="")
    coupon_code = Column(String, default="")
    discount_toman = Column(Integer, default=0)
    subtotal_toman = Column(Integer, default=0)
    shipping_fee_toman = Column(Integer, default=45000)
    total_toman = Column(Integer, default=0)
    order_status = Column(String, default="pending")
    payment_status = Column(String, default="pending")
    payment_ref = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=True)
    product_title = Column(String, default="")
    variant_title = Column(String, default="")
    qty = Column(Integer, default=1)
    unit_price_toman = Column(Integer, default=0)
    row_total_toman = Column(Integer, default=0)
    order = relationship("Order", back_populates="items")

class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    excerpt = Column(Text, default="")
    content = Column(Text, default="")
    cover_image = Column(String, default="")
    author = Column(String, default="نوار")
    category = Column(String, default="عمومی")
    read_time = Column(String, default="۵ دقیقه")
    is_published = Column(Boolean, default=True)
    published_on = Column(String, default="")
    display_order = Column(Integer, default=0)
    seo_title = Column(String, default="")
    seo_description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class Faq(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

class ProductFaq(Base):
    __tablename__ = "product_faqs"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    display_order = Column(Integer, default=0)
    product = relationship("Product", back_populates="faqs")

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, default="percent")
    value = Column(Float, default=10)
    label = Column(String, default="")
    min_order = Column(Integer, default=0)
    max_uses = Column(Integer, default=0)
    used_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    expiry = Column(String, default="")

class NavigationLink(Base):
    __tablename__ = "navigation_links"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    route = Column(String, nullable=False)
    placement = Column(String, default="header")
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

class SiteSetting(Base):
    __tablename__ = "site_settings"
    key = Column(String, primary_key=True)
    value = Column(Text, default="")

class Wishlist(Base):
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user = relationship("User", back_populates="wishlist")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_name = Column(String, default="کاربر")
    rating = Column(Integer, default=5)
    text = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

class ReturnRequest(Base):
    __tablename__ = "return_requests"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    order_ref = Column(String, default="")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reason = Column(String, default="")
    description = Column(Text, default="")
    items_json = Column(Text, default="[]")
    total_amount = Column(Integer, default=0)
    status = Column(String, default="در انتظار بررسی")
    admin_note = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="خانه")
    recipient_name = Column(String, default="")
    mobile = Column(String, default="")
    province = Column(String, default="")
    city = Column(String, default="")
    address_line = Column(Text, default="")
    postal_code = Column(String, default="")
    is_default = Column(Boolean, default=False)
    user = relationship("User", back_populates="addresses")

Base.metadata.create_all(bind=engine)

# ─── Helpers ─────────────────────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(pw: str) -> str:
    salt = SECRET_KEY.encode()
    return hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, 100000).hex()

def verify_password(plain: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(plain), hashed)

def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    return pyjwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[int]:
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except (InvalidTokenError, Exception):
        return None

def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if not creds:
        return None
    uid = decode_token(creds.credentials)
    if not uid:
        return None
    return db.query(User).filter(User.id == uid).first()

def require_user(user: Optional[User] = Depends(get_current_user)) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="احراز هویت لازم است")
    return user

def require_admin(user: Optional[User] = Depends(get_current_user)) -> User:
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="دسترسی مجاز نیست")
    return user

def _j(val: str | None) -> Any:
    try:
        return json.loads(val or "[]")
    except Exception:
        return []

def _jd(val: str | None) -> Any:
    try:
        return json.loads(val or "{}")
    except Exception:
        return {}

def slugify(text: str) -> str:
    value = "-".join((text or "").strip().lower().split())
    value = re.sub(r"[^a-z0-9\u0600-\u06FF-]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")

def _effective_price(price: int, discount: int) -> int:
    return max(price - max(0, discount), 0)

def _cat_payload(cat: Category) -> dict:
    return {
        "id": cat.id, "name": cat.name, "slug": cat.slug,
        "parent_id": cat.parent_id, "icon": cat.icon, "color": cat.color,
        "image": cat.image, "description": cat.description,
        "display_order": cat.display_order, "is_active": cat.is_active,
        "has_variants": cat.has_variants, "variant_label": cat.variant_label,
        "has_grinds": cat.has_grinds,
        "default_variants": _j(cat.default_variants_json),
        "default_grinds": _j(cat.default_grinds_json),
        "attributes": _j(cat.attributes_json),
    }

def _variant_payload(v: ProductVariant) -> dict:
    price = v.price_toman
    discount = v.discount_toman
    return {
        "id": v.id, "product_id": v.product_id, "title": v.title, "sku": v.sku,
        "image": v.image, "price_toman": price, "discount_toman": discount,
        "effective_price_toman": _effective_price(price, discount),
        "stock_qty": v.stock_qty, "display_order": v.display_order,
        "is_published": v.is_published, "attributes": _jd(v.attributes_json),
    }

def _product_payload(p: Product, include_variants: bool = True, db: Session = None) -> dict:
    price = p.price_toman
    discount = p.discount_toman
    effective = _effective_price(price, discount)
    variants = []
    if include_variants and p.has_variants and db:
        vs = db.query(ProductVariant).filter(
            ProductVariant.product_id == p.id, ProductVariant.is_published == True
        ).order_by(ProductVariant.display_order).all()
        variants = [_variant_payload(v) for v in vs]
        if variants:
            effective = min(v["effective_price_toman"] for v in variants)
    cat_name = p.category.name if p.category else ""
    cat_slug = p.category.slug if p.category else ""
    return {
        "id": p.id, "name": p.name, "slug": p.slug,
        "category_id": p.category_id, "category_name": cat_name, "category_slug": cat_slug,
        "short_description": p.short_description, "description": p.description,
        "price_toman": price, "discount_toman": discount, "effective_price_toman": effective,
        "stock_qty": p.stock_qty, "has_variants": p.has_variants,
        "image": p.image, "gallery": _j(p.gallery_json),
        "is_featured": p.is_featured, "is_published": p.is_published,
        "display_order": p.display_order, "sku": p.sku,
        "seo_title": p.seo_title, "seo_description": p.seo_description,
        "specs": _j(p.specs_json), "notes": _j(p.notes_json),
        "flavor": _jd(p.flavor_json),
        "variants": variants,
        "created_at": p.created_at.isoformat() if p.created_at else "",
    }

def _order_payload(o: Order) -> dict:
    return {
        "id": o.id, "ref": o.ref, "user_id": o.user_id,
        "customer_name": o.customer_name, "mobile": o.mobile,
        "shipping_address": o.shipping_address, "notes": o.notes,
        "coupon_code": o.coupon_code, "discount_toman": o.discount_toman,
        "subtotal_toman": o.subtotal_toman, "shipping_fee_toman": o.shipping_fee_toman,
        "total_toman": o.total_toman,
        "order_status": o.order_status, "payment_status": o.payment_status,
        "payment_ref": o.payment_ref,
        "created_at": o.created_at.isoformat() if o.created_at else "",
        "items": [
            {
                "id": i.id, "product_id": i.product_id, "variant_id": i.variant_id,
                "product_title": i.product_title, "variant_title": i.variant_title,
                "qty": i.qty, "unit_price_toman": i.unit_price_toman,
                "row_total_toman": i.row_total_toman,
            }
            for i in (o.items or [])
        ],
    }

def _get_setting(db: Session, key: str, default: str = "") -> str:
    row = db.query(SiteSetting).filter(SiteSetting.key == key).first()
    return row.value if row else default

def _set_setting(db: Session, key: str, value: str):
    row = db.query(SiteSetting).filter(SiteSetting.key == key).first()
    if row:
        row.value = value
    else:
        db.add(SiteSetting(key=key, value=value))

# ─── Seed ─────────────────────────────────────────────────────────────────────
def _seed(db: Session):
    if db.query(User).first():
        return
    admin = User(
        full_name="مدیر سیستم", email="admin@coffeeyar.ir",
        password_hash=hash_password("admin1234"), is_admin=True
    )
    db.add(admin)

    cats_data = [
        {"name": "قهوه", "slug": "coffee", "icon": "☕", "color": "#6b4226", "has_variants": True, "variant_label": "وزن", "has_grinds": True,
         "default_variants": [{"label": "۲۵۰ گرم", "multiplier": 1}, {"label": "۵۰۰ گرم", "multiplier": 1.9}, {"label": "۱ کیلوگرم", "multiplier": 3.5}],
         "default_grinds": ["دانه کامل", "اسپرسو", "موکاپات", "فرنچ پرس", "V60"],
         "attributes": [{"key": "origin", "label": "خاستگاه", "type": "text"}, {"key": "roast", "label": "درجه برشته", "type": "select", "options": ["روشن", "متوسط", "تیره"]}, {"key": "process", "label": "فرآوری", "type": "select", "options": ["شسته", "نچرال", "هانی"]}]},
        {"name": "قهوه تک‌خاستگاه", "slug": "single-origin", "icon": "🌱", "color": "#6b4226", "parent_slug": "coffee"},
        {"name": "بلند قهوه", "slug": "blend", "icon": "🔀", "color": "#6b4226", "parent_slug": "coffee"},
        {"name": "اکسسوری", "slug": "accessories", "icon": "🫖", "color": "#8b6914",
         "attributes": [{"key": "brand", "label": "برند", "type": "text"}, {"key": "material", "label": "جنس", "type": "text"}]},
        {"name": "وسایل دم‌آوری", "slug": "brewing", "icon": "🫗", "color": "#8b6914", "parent_slug": "accessories"},
        {"name": "آسیاب", "slug": "grinder", "icon": "⚙️", "color": "#8b6914", "parent_slug": "accessories"},
    ]
    cat_objs: dict[str, Category] = {}
    for cd in cats_data:
        c = Category(
            name=cd["name"], slug=cd["slug"], icon=cd.get("icon", "📦"), color=cd.get("color", "#6b7280"),
            has_variants=cd.get("has_variants", False), variant_label=cd.get("variant_label", ""),
            has_grinds=cd.get("has_grinds", False),
            default_variants_json=json.dumps(cd.get("default_variants", []), ensure_ascii=False),
            default_grinds_json=json.dumps(cd.get("default_grinds", []), ensure_ascii=False),
            attributes_json=json.dumps(cd.get("attributes", []), ensure_ascii=False),
        )
        db.add(c)
        db.flush()
        if "parent_slug" in cd and cd["parent_slug"] in cat_objs:
            c.parent_id = cat_objs[cd["parent_slug"]].id
        cat_objs[cd["slug"]] = c

    prods_data = [
        {"name": "اتیوپی یرگاچف", "slug": "ethiopia-yirgacheffe", "cat": "single-origin", "price": 480000,
         "short": "قهوه روشن و معطر با یادداشت‌های گل و میوه", "stock": 24,
         "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600&q=80",
         "desc": "یک قهوه‌ی روشن و معطر از منطقه‌ی یرگاچف اتیوپی با اسیدیته‌ی روشن و عطر گل‌های سفید.",
         "notes": ["یاسمن", "لیمو", "عسل"], "flavor": {"bitterness": 3, "acidity": 8, "aroma": 9},
         "specs": [{"label": "خاستگاه", "value": "اتیوپی — یرگاچف"}, {"label": "فرآوری", "value": "شسته"}, {"label": "رست", "value": "روشن"}, {"label": "اسیدیته", "value": "۸/۱۰"}]},
        {"name": "کلمبیا هویلا", "slug": "colombia-huila", "cat": "single-origin", "price": 420000,
         "short": "قهوه متوسط با شیرینی کارامل", "stock": 5,
         "image": "https://images.unsplash.com/photo-1611854779393-1b2da9d400fe?w=600&q=80",
         "desc": "قهوه‌ای با شیرینی طبیعی کارامل از دامنه‌های بلند کلمبیا.",
         "notes": ["کارامل", "شکلات", "آلو"], "flavor": {"bitterness": 4, "acidity": 6, "aroma": 8},
         "specs": [{"label": "خاستگاه", "value": "کلمبیا — هویلا"}, {"label": "فرآوری", "value": "شسته"}, {"label": "رست", "value": "متوسط"}]},
        {"name": "کنیا AA", "slug": "kenya-aa", "cat": "single-origin", "price": 520000,
         "short": "قهوه با اسیدیته شراب‌گون و طعم میوه‌های قرمز", "stock": 12, "is_featured": True,
         "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=600&q=80",
         "desc": "یکی از بهترین قهوه‌های تک‌خاستگاه با پروفایل طعمی بی‌نظیر.",
         "notes": ["توت سیاه", "گریپ‌فروت", "شراب قرمز"], "flavor": {"bitterness": 3, "acidity": 9, "aroma": 9},
         "specs": [{"label": "خاستگاه", "value": "کنیا"}, {"label": "رست", "value": "روشن تا متوسط"}]},
        {"name": "بلند اسپرسو نوار", "slug": "navar-espresso-blend", "cat": "blend", "price": 390000,
         "short": "بلند اسپرسو خانگی نوار با تعادل طعم و عطر", "stock": 30, "is_featured": True,
         "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=600&q=80",
         "desc": "بلند اسپرسو اختصاصی نوار، ترکیبی از قهوه‌های برزیل و اتیوپی با طعم متعادل.",
         "notes": ["شکلات تلخ", "بادام", "کارامل"], "flavor": {"bitterness": 7, "acidity": 4, "aroma": 8},
         "specs": [{"label": "ترکیب", "value": "برزیل + اتیوپی"}, {"label": "رست", "value": "متوسط تیره"}]},
        {"name": "فرنچ پرس کلاسیک", "slug": "french-press-classic", "cat": "brewing", "price": 350000,
         "short": "فرنچ پرس شیشه‌ای با کیفیت بالا", "stock": 15,
         "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80",
         "desc": "فرنچ پرس کلاسیک با بدنه شیشه‌ای مقاوم و فیلتر استینلس استیل.",
         "specs": [{"label": "ظرفیت", "value": "۳۵۰ میلی‌لیتر"}, {"label": "جنس", "value": "شیشه بروسیلیکات"}]},
        {"name": "کتری ماهیچه‌ای برقی", "slug": "gooseneck-kettle", "cat": "brewing", "price": 890000,
         "short": "کتری دقیق برای دم‌آوری حرفه‌ای", "stock": 8, "is_featured": True,
         "image": "https://images.unsplash.com/photo-1521302200778-33500795e128?w=600&q=80",
         "desc": "کتری ماهیچه‌ای برقی با کنترل دمای دقیق برای دم‌آوری حرفه‌ای.",
         "specs": [{"label": "ظرفیت", "value": "۶۰۰ میلی‌لیتر"}, {"label": "کنترل دما", "value": "۶۰ تا ۱۰۰ درجه"}]},
    ]
    for pd in prods_data:
        cat = cat_objs.get(pd["cat"])
        p = Product(
            name=pd["name"], slug=pd["slug"], category_id=cat.id if cat else None,
            price_toman=pd["price"], short_description=pd.get("short", ""),
            description=pd.get("desc", ""), stock_qty=pd.get("stock", 10),
            is_featured=pd.get("is_featured", False), is_published=True,
            image=pd.get("image", ""),
            notes_json=json.dumps(pd.get("notes", []), ensure_ascii=False),
            flavor_json=json.dumps(pd.get("flavor", {}), ensure_ascii=False),
            specs_json=json.dumps(pd.get("specs", []), ensure_ascii=False),
        )
        db.add(p)

    for q, a in [
        ("قهوه‌های شما تازه برشته شده هستند؟", "بله، تمام قهوه‌های ما در کارگاه کوچک خودمان برشته می‌شوند و در کمتر از یک هفته ارسال می‌گردند."),
        ("ارسال به تمام شهرهای ایران دارید؟", "بله، ارسال به تمام نقاط ایران از طریق پست و پیک انجام می‌شود."),
        ("تفاوت آسیاب‌های مختلف در چیست؟", "هر روش دم‌آوری نیاز به درجه خاصی از آسیاب دارد. هنگام سفارش می‌توانید درجه آسیاب را انتخاب کنید."),
        ("آیا امکان مرجوع کردن محصول وجود دارد؟", "اگر محصول دریافتی با توضیحات مطابقت نداشته باشد، تا ۷۲ ساعت پس از دریافت قابل مرجوع است."),
        ("هزینه ارسال چقدر است؟", "هزینه ارسال عادی ۴۵٬۰۰۰ تومان است و برای سفارش‌های بالای ۵۰۰٬۰۰۰ تومان رایگان می‌شود."),
    ]:
        db.add(Faq(question=q, answer=a))

    for code, t, v, lbl, mn in [
        ("NAVAR10", "percent", 10, "۱۰٪ تخفیف", 0),
        ("NAVAR20", "percent", 20, "۲۰٪ تخفیف", 500000),
        ("WELCOME", "percent", 15, "۱۵٪ تخفیف خوش‌آمدگویی", 0),
    ]:
        db.add(Coupon(code=code, type=t, value=v, label=lbl, min_order=mn, max_uses=100, is_active=True))

    for label, route, placement, order in [
        ("خانه", "/", "header", 0), ("محصولات", "/products", "header", 1),
        ("بلاگ", "/blog", "header", 2), ("درباره ما", "/about", "header", 3),
        ("تماس", "/contact", "header", 4),
        ("درباره ما", "/about", "footer", 0), ("تماس با ما", "/contact", "footer", 1),
        ("سوالات متداول", "/faq", "footer", 2), ("قوانین", "/policies", "footer", 3),
    ]:
        db.add(NavigationLink(label=label, route=route, placement=placement, display_order=order))

    settings = {
        "shop_name": "نوار", "description": "قهوه‌ی تخصصی، تازه برشته شده.", "phone": "",
        "email": "", "address": "", "instagram": "#", "telegram": "#", "enamad_code": "",
        "shipping_standard_price": "45000", "shipping_standard_free_threshold": "500000",
        "shipping_express_price": "90000", "shipping_express_free_threshold": "0",
        "payment_online": "true", "payment_cod": "true",
    }
    for k, v in settings.items():
        db.add(SiteSetting(key=k, value=v))

    reviews_data = [
        ("ethiopia-yirgacheffe", "سارا احمدی", 5, "بهترین قهوه‌ای که تا حالا خوردم. عطر یاسمن واقعاً حس می‌شه."),
        ("ethiopia-yirgacheffe", "علی رضایی", 4, "اسیدیته‌ی روشن و تازه. برشته‌ش خوبه."),
        ("colombia-huila", "مریم محمدی", 5, "شیرینی کارامل واقعیه. برای صبح‌ها با موکاپات خیلی خوبه."),
        ("kenya-aa", "کیوان نجفی", 5, "این قهوه یه تجربه‌ی کاملاً متفاوته. اسیدیته‌ی شراب‌گون فوق‌العاده‌ست."),
    ]

    for slug, name, rating, text in reviews_data:
        prod = db.query(Product).filter(Product.slug == slug).first()
        if prod:
            db.add(Review(product_id=prod.id, user_name=name, rating=rating, text=text))

    for title, slug, excerpt, body, cat, rt in [
        ("هنر دم‌آوری دستی", "art-of-pour-over", "راهنمای کامل برای دم‌آوری بهتر", "دم‌آوری دستی یک هنر است...", "دم‌آوری", "۵ دقیقه"),
        ("راهنمای دم‌آوری با فرنچ پرس", "french-press-guide", "همه چیز درباره فرنچ پرس", "فرنچ پرس یکی از محبوب‌ترین...", "دم‌آوری", "۴ دقیقه"),
        ("تفاوت قهوه‌های تک‌خاستگاه", "single-origin-vs-blend", "کدام را انتخاب کنیم؟", "قهوه تک‌خاستگاه...", "آموزش", "۶ دقیقه"),
    ]:
        db.add(BlogPost(title=title, slug=slug, excerpt=excerpt, content=body,
                       category=cat, read_time=rt, is_published=True,
                       published_on=datetime.now().strftime("%Y-%m-%d")))

    db.commit()

# ─── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="Coffeeyar API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        _seed(db)
    finally:
        db.close()

# ─── Pydantic schemas ─────────────────────────────────────────────────────────
class RegisterIn(BaseModel):
    name: str
    email: str
    phone: str = ""
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

class UpdateProfileIn(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class AddressIn(BaseModel):
    title: str = "خانه"
    recipient_name: str = ""
    mobile: str = ""
    province: str = ""
    city: str = ""
    address_line: str = ""
    postal_code: str = ""
    is_default: bool = False

class OrderIn(BaseModel):
    customer_name: str
    mobile: str
    shipping_address: str = ""
    notes: str = ""
    coupon_code: str = ""
    payment_method: str = "cod"
    items: list[dict] = []

class ReviewIn(BaseModel):
    product_id: int
    user_name: str = ""
    rating: int = 5
    text: str = ""

class CouponValidateIn(BaseModel):
    code: str
    order_total: int

class ReturnIn(BaseModel):
    order_id: Optional[int] = None
    order_ref: str = ""
    reason: str = ""
    description: str = ""
    items: list[dict] = []
    total_amount: int = 0

class FaqIn(BaseModel):
    question: str
    answer: str
    display_order: int = 0
    is_active: bool = True

class CouponIn(BaseModel):
    code: str
    type: str = "percent"
    value: float = 10
    label: str = ""
    min_order: int = 0
    max_uses: int = 100
    is_active: bool = True
    expiry: str = ""

class NavLinkIn(BaseModel):
    label: str
    route: str
    placement: str = "header"
    display_order: int = 0
    is_active: bool = True

class BlogPostIn(BaseModel):
    title: str
    slug: str = ""
    excerpt: str = ""
    content: str = ""
    cover_image: str = ""
    author: str = "نوار"
    category: str = "عمومی"
    read_time: str = "۵ دقیقه"
    is_published: bool = True
    seo_title: str = ""
    seo_description: str = ""

class ProductIn(BaseModel):
    name: str
    slug: str = ""
    category_id: Optional[int] = None
    short_description: str = ""
    description: str = ""
    price_toman: int = 0
    discount_toman: int = 0
    stock_qty: int = 0
    has_variants: bool = False
    image: str = ""
    gallery_json: str = "[]"
    is_featured: bool = False
    is_published: bool = True
    display_order: int = 0
    sku: str = ""
    specs_json: str = "[]"
    notes_json: str = "[]"
    flavor_json: str = "{}"
    seo_title: str = ""
    seo_description: str = ""

class CategoryIn(BaseModel):
    name: str
    slug: str = ""
    parent_id: Optional[int] = None
    icon: str = "📦"
    color: str = "#6b7280"
    image: str = ""
    description: str = ""
    display_order: int = 0
    has_variants: bool = False
    variant_label: str = ""
    has_grinds: bool = False
    default_variants_json: str = "[]"
    default_grinds_json: str = "[]"
    attributes_json: str = "[]"
    is_active: bool = True

# ─── Auth Routes ─────────────────────────────────────────────────────────────
@app.post("/api/auth/register")
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "این ایمیل قبلاً ثبت شده است")
    user = User(
        full_name=body.name, email=body.email,
        phone=body.phone, password_hash=hash_password(body.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.id)
    return {"token": token, "user": {"id": user.id, "name": user.full_name, "email": user.email, "phone": user.phone, "is_admin": user.is_admin}}

@app.post("/api/auth/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "ایمیل یا رمز عبور اشتباه است")
    token = create_token(user.id)
    return {"token": token, "user": {"id": user.id, "name": user.full_name, "email": user.email, "phone": user.phone, "is_admin": user.is_admin}}

@app.get("/api/auth/me")
def me(user: User = Depends(require_user)):
    return {"id": user.id, "name": user.full_name, "email": user.email, "phone": user.phone, "is_admin": user.is_admin}

@app.put("/api/auth/me")
def update_me(body: UpdateProfileIn, user: User = Depends(require_user), db: Session = Depends(get_db)):
    if body.full_name: user.full_name = body.full_name
    if body.phone is not None: user.phone = body.phone
    if body.password: user.password_hash = hash_password(body.password)
    db.commit()
    return {"id": user.id, "name": user.full_name, "email": user.email, "phone": user.phone}

# ─── Addresses ───────────────────────────────────────────────────────────────
@app.get("/api/addresses")
def get_addresses(user: User = Depends(require_user), db: Session = Depends(get_db)):
    addrs = db.query(Address).filter(Address.user_id == user.id).all()
    return [{"id": a.id, "title": a.title, "recipient_name": a.recipient_name, "mobile": a.mobile,
             "province": a.province, "city": a.city, "address_line": a.address_line,
             "postal_code": a.postal_code, "is_default": a.is_default} for a in addrs]

@app.post("/api/addresses")
def add_address(body: AddressIn, user: User = Depends(require_user), db: Session = Depends(get_db)):
    if body.is_default:
        db.query(Address).filter(Address.user_id == user.id).update({"is_default": False})
    addr = Address(user_id=user.id, **body.model_dump())
    db.add(addr)
    db.commit()
    db.refresh(addr)
    return {"id": addr.id, **body.model_dump()}

@app.delete("/api/addresses/{addr_id}")
def delete_address(addr_id: int, user: User = Depends(require_user), db: Session = Depends(get_db)):
    addr = db.query(Address).filter(Address.id == addr_id, Address.user_id == user.id).first()
    if not addr:
        raise HTTPException(404, "آدرس یافت نشد")
    db.delete(addr)
    db.commit()
    return {"ok": True}

# ─── Categories ──────────────────────────────────────────────────────────────
@app.get("/api/categories")
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(Category).filter(Category.is_active == True).order_by(Category.display_order).all()
    return [_cat_payload(c) for c in cats]

# ─── Products ─────────────────────────────────────────────────────────────────
@app.get("/api/products")
def list_products(
    category_slug: str = "", featured: bool = False, in_stock: bool = False,
    sort: str = "default", page: int = 1, page_size: int = 24,
    db: Session = Depends(get_db)
):
    q = db.query(Product).filter(Product.is_published == True)
    if featured:
        q = q.filter(Product.is_featured == True)
    if in_stock:
        q = q.filter(Product.stock_qty > 0)
    if category_slug:
        cat = db.query(Category).filter(Category.slug == category_slug).first()
        if cat:
            cat_ids = [cat.id]
            children = db.query(Category).filter(Category.parent_id == cat.id).all()
            cat_ids.extend(c.id for c in children)
            q = q.filter(Product.category_id.in_(cat_ids))
    if sort == "price_asc":
        q = q.order_by(Product.price_toman.asc())
    elif sort == "price_desc":
        q = q.order_by(Product.price_toman.desc())
    elif sort == "newest":
        q = q.order_by(Product.created_at.desc())
    else:
        q = q.order_by(Product.display_order.asc(), Product.created_at.desc())
    total = q.count()
    prods = q.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [_product_payload(p, include_variants=False) for p in prods],
        "total": total, "page": page, "page_size": page_size,
        "has_next": (page * page_size) < total,
    }

@app.get("/api/products/{slug}")
def get_product(slug: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.slug == slug, Product.is_published == True).first()
    if not p:
        raise HTTPException(404, "محصول یافت نشد")
    return _product_payload(p, include_variants=True, db=db)

@app.get("/api/products/{slug}/faqs")
def get_product_faqs(slug: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.slug == slug).first()
    if not p:
        return []
    return [{"id": f.id, "question": f.question, "answer": f.answer} for f in p.faqs]

# ─── Reviews ─────────────────────────────────────────────────────────────────
@app.get("/api/reviews/{product_id}")
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    revs = db.query(Review).filter(Review.product_id == product_id).order_by(Review.created_at.desc()).all()
    return [{"id": r.id, "user_name": r.user_name, "rating": r.rating, "text": r.text,
             "created_at": r.created_at.isoformat() if r.created_at else ""} for r in revs]

@app.post("/api/reviews")
def add_review(body: ReviewIn, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    user_name = body.user_name or (user.full_name if user else "کاربر مهمان")
    rev = Review(product_id=body.product_id, user_id=user.id if user else None,
                 user_name=user_name, rating=body.rating, text=body.text)
    db.add(rev)
    db.commit()
    db.refresh(rev)
    return {"id": rev.id, "user_name": rev.user_name, "rating": rev.rating, "text": rev.text}

# ─── Wishlist ────────────────────────────────────────────────────────────────
@app.get("/api/wishlist")
def get_wishlist(user: User = Depends(require_user), db: Session = Depends(get_db)):
    items = db.query(Wishlist).filter(Wishlist.user_id == user.id).all()
    ids = [w.product_id for w in items]
    prods = db.query(Product).filter(Product.id.in_(ids)).all()
    return [_product_payload(p, include_variants=False) for p in prods]

@app.post("/api/wishlist/{product_id}")
def toggle_wishlist(product_id: int, user: User = Depends(require_user), db: Session = Depends(get_db)):
    existing = db.query(Wishlist).filter(Wishlist.user_id == user.id, Wishlist.product_id == product_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {"wishlisted": False}
    db.add(Wishlist(user_id=user.id, product_id=product_id))
    db.commit()
    return {"wishlisted": True}

@app.get("/api/wishlist/ids")
def get_wishlist_ids(user: User = Depends(require_user), db: Session = Depends(get_db)):
    items = db.query(Wishlist).filter(Wishlist.user_id == user.id).all()
    return {"ids": [w.product_id for w in items]}

# ─── Coupons ─────────────────────────────────────────────────────────────────
@app.post("/api/coupons/validate")
def validate_coupon(body: CouponValidateIn, db: Session = Depends(get_db)):
    c = db.query(Coupon).filter(Coupon.code == body.code.strip().upper()).first()
    if not c:
        raise HTTPException(400, "کد تخفیف نامعتبر است")
    if not c.is_active:
        raise HTTPException(400, "این کد تخفیف غیرفعال است")
    if c.min_order and body.order_total < c.min_order:
        raise HTTPException(400, f"حداقل خرید برای این کد {c.min_order:,} تومان است")
    if c.max_uses and c.used_count >= c.max_uses:
        raise HTTPException(400, "ظرفیت استفاده از این کد تمام شده است")
    if c.expiry:
        try:
            if datetime.strptime(c.expiry, "%Y-%m-%d") < datetime.now():
                raise HTTPException(400, "این کد تخفیف منقضی شده است")
        except ValueError:
            pass
    discount = 0
    if c.type == "percent":
        discount = int(body.order_total * c.value / 100)
    else:
        discount = int(c.value)
    return {"ok": True, "code": c.code, "type": c.type, "value": c.value, "label": c.label, "discount": discount}

# ─── Orders ──────────────────────────────────────────────────────────────────
@app.post("/api/orders")
def create_order(body: OrderIn, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    if not body.customer_name or not body.mobile:
        raise HTTPException(400, "نام و شماره موبایل الزامی است")
    if not body.items:
        raise HTTPException(400, "سبد خرید خالی است")

    std_price = int(_get_setting(db, "shipping_standard_price", "45000"))
    order_items = []
    subtotal = 0
    for raw in body.items:
        pid = raw.get("product_id") or raw.get("id")
        vid = raw.get("variant_id")
        qty = max(int(raw.get("qty", 1)), 1)
        p = db.query(Product).filter(Product.id == pid).first() if pid else None
        if not p:
            p = db.query(Product).filter(Product.slug == str(pid)).first()
        if not p:
            raise HTTPException(400, f"محصول یافت نشد: {pid}")
        variant = None
        if vid:
            variant = db.query(ProductVariant).filter(ProductVariant.id == vid, ProductVariant.product_id == p.id).first()
        if variant:
            unit_price = _effective_price(variant.price_toman or p.price_toman, variant.discount_toman or p.discount_toman)
        else:
            unit_price = _effective_price(p.price_toman, p.discount_toman)
        row_total = unit_price * qty
        subtotal += row_total
        order_items.append(OrderItem(
            product_id=p.id, variant_id=variant.id if variant else None,
            product_title=p.name, variant_title=variant.title if variant else "",
            qty=qty, unit_price_toman=unit_price, row_total_toman=row_total,
        ))

    coupon_discount = 0
    coupon_code = ""
    if body.coupon_code:
        c = db.query(Coupon).filter(Coupon.code == body.coupon_code.strip().upper(), Coupon.is_active == True).first()
        if c:
            coupon_code = c.code
            if c.type == "percent":
                coupon_discount = int(subtotal * c.value / 100)
            else:
                coupon_discount = int(c.value)
            c.used_count += 1

    total = max(subtotal + std_price - coupon_discount, 0)
    ref = "NV-" + secrets.token_hex(3).upper()
    order = Order(
        ref=ref, user_id=user.id if user else None,
        customer_name=body.customer_name, mobile=body.mobile,
        shipping_address=body.shipping_address, notes=body.notes,
        coupon_code=coupon_code, discount_toman=coupon_discount,
        subtotal_toman=subtotal, shipping_fee_toman=std_price, total_toman=total,
        order_status="pending", payment_status="pending" if body.payment_method == "online" else "cod",
    )
    db.add(order)
    db.flush()
    for item in order_items:
        item.order_id = order.id
        db.add(item)
    db.commit()
    db.refresh(order)
    return _order_payload(order)

@app.get("/api/orders")
def get_orders(user: User = Depends(require_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()
    return [_order_payload(o) for o in orders]

@app.get("/api/orders/{order_ref}")
def get_order(order_ref: str, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    o = db.query(Order).filter(Order.ref == order_ref).first()
    if not o:
        raise HTTPException(404, "سفارش یافت نشد")
    return _order_payload(o)

# ─── Returns ─────────────────────────────────────────────────────────────────
@app.post("/api/returns")
def create_return(body: ReturnIn, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user)):
    ret = ReturnRequest(
        order_id=body.order_id, order_ref=body.order_ref,
        user_id=user.id if user else None,
        reason=body.reason, description=body.description,
        items_json=json.dumps(body.items, ensure_ascii=False),
        total_amount=body.total_amount,
    )
    db.add(ret)
    db.commit()
    db.refresh(ret)
    return {"id": ret.id, "status": ret.status, "created_at": ret.created_at.isoformat()}

@app.get("/api/returns")
def get_returns(user: User = Depends(require_user), db: Session = Depends(get_db)):
    rets = db.query(ReturnRequest).filter(ReturnRequest.user_id == user.id).order_by(ReturnRequest.created_at.desc()).all()
    return [{"id": r.id, "order_ref": r.order_ref, "reason": r.reason, "status": r.status,
             "total_amount": r.total_amount, "admin_note": r.admin_note,
             "created_at": r.created_at.isoformat()} for r in rets]

# ─── FAQ ─────────────────────────────────────────────────────────────────────
@app.get("/api/faq")
def get_faq(db: Session = Depends(get_db)):
    faqs = db.query(Faq).filter(Faq.is_active == True).order_by(Faq.display_order).all()
    return [{"id": f.id, "question": f.question, "answer": f.answer} for f in faqs]

# ─── Blog ────────────────────────────────────────────────────────────────────
@app.get("/api/blog")
def list_blog(page: int = 1, page_size: int = 12, db: Session = Depends(get_db)):
    q = db.query(BlogPost).filter(BlogPost.is_published == True).order_by(BlogPost.display_order, BlogPost.created_at.desc())
    total = q.count()
    posts = q.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [{"id": p.id, "title": p.title, "slug": p.slug, "excerpt": p.excerpt,
                   "cover_image": p.cover_image, "author": p.author, "category": p.category,
                   "read_time": p.read_time, "published_on": p.published_on,
                   "is_published": p.is_published,
                   "created_at": p.created_at.isoformat()} for p in posts],
        "total": total, "page": page,
    }

@app.get("/api/blog/{slug}")
def get_blog_post(slug: str, db: Session = Depends(get_db)):
    p = db.query(BlogPost).filter(BlogPost.slug == slug, BlogPost.is_published == True).first()
    if not p:
        raise HTTPException(404, "مطلب یافت نشد")
    return {"id": p.id, "title": p.title, "slug": p.slug, "excerpt": p.excerpt,
            "content": p.content, "cover_image": p.cover_image, "author": p.author,
            "category": p.category, "read_time": p.read_time, "published_on": p.published_on,
            "seo_title": p.seo_title, "seo_description": p.seo_description,
            "created_at": p.created_at.isoformat()}

# ─── Site Settings & Navigation ──────────────────────────────────────────────
@app.get("/api/site-settings")
def get_site_settings(db: Session = Depends(get_db)):
    rows = db.query(SiteSetting).all()
    raw = {r.key: r.value for r in rows}
    return {
        "shop_name": raw.get("shop_name", "نوار"),
        "description": raw.get("description", ""),
        "phone": raw.get("phone", ""),
        "email": raw.get("email", ""),
        "address": raw.get("address", ""),
        "instagram": raw.get("instagram", "#"),
        "telegram": raw.get("telegram", "#"),
        "enamad_code": raw.get("enamad_code", ""),
        "payment_online": raw.get("payment_online", "true") == "true",
        "payment_cod": raw.get("payment_cod", "true") == "true",
        "shipping": {
            "standard": {
                "enabled": True, "label": "ارسال عادی", "days": "۲ تا ۴ روز کاری",
                "price": int(raw.get("shipping_standard_price", "45000")),
                "free_threshold": int(raw.get("shipping_standard_free_threshold", "500000")),
            },
            "express": {
                "enabled": True, "label": "ارسال اکسپرس", "days": "۲۴ ساعته",
                "price": int(raw.get("shipping_express_price", "90000")),
                "free_threshold": int(raw.get("shipping_express_free_threshold", "0")),
            },
        },
    }

@app.get("/api/navigation")
def get_navigation(db: Session = Depends(get_db)):
    links = db.query(NavigationLink).filter(NavigationLink.is_active == True).order_by(NavigationLink.display_order).all()
    result: dict[str, list] = {"header": [], "footer": [], "mobile": []}
    for l in links:
        p = l.placement if l.placement in result else "header"
        result[p].append({"id": l.id, "label": l.label, "route": l.route})
    return result

# ─── Admin – Dashboard ───────────────────────────────────────────────────────
@app.get("/api/admin/dashboard")
def admin_dashboard(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return {
        "total_products": db.query(Product).count(),
        "total_orders": db.query(Order).count(),
        "total_customers": db.query(User).filter(User.is_admin == False).count(),
        "total_revenue": db.query(Order).with_entities(Order.total_toman).filter(Order.payment_status == "paid").all(),
        "recent_orders": [_order_payload(o) for o in db.query(Order).order_by(Order.created_at.desc()).limit(5).all()],
        "pending_returns": db.query(ReturnRequest).filter(ReturnRequest.status == "در انتظار بررسی").count(),
    }

# ─── Admin – Products ────────────────────────────────────────────────────────
@app.get("/api/admin/products")
def admin_products(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    prods = db.query(Product).order_by(Product.display_order, Product.created_at.desc()).all()
    return [_product_payload(p, include_variants=False) for p in prods]

@app.post("/api/admin/products")
def admin_create_product(body: ProductIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    slug = body.slug or slugify(body.name) or ("product-" + secrets.token_hex(4))
    p = Product(slug=slug, **{k: v for k, v in body.model_dump().items() if k != "slug"})
    db.add(p)
    db.commit()
    db.refresh(p)
    return _product_payload(p, include_variants=True, db=db)

@app.put("/api/admin/products/{pid}")
def admin_update_product(pid: int, body: ProductIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == pid).first()
    if not p:
        raise HTTPException(404, "محصول یافت نشد")
    for k, v in body.model_dump().items():
        setattr(p, k, v)
    if not p.slug:
        p.slug = slugify(p.name)
    db.commit()
    return _product_payload(p, include_variants=True, db=db)

@app.delete("/api/admin/products/{pid}")
def admin_delete_product(pid: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == pid).first()
    if not p:
        raise HTTPException(404, "محصول یافت نشد")
    db.delete(p)
    db.commit()
    return {"ok": True}

# ─── Admin – Categories ──────────────────────────────────────────────────────
@app.get("/api/admin/categories")
def admin_categories(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    cats = db.query(Category).order_by(Category.display_order).all()
    return [_cat_payload(c) for c in cats]

@app.post("/api/admin/categories")
def admin_create_category(body: CategoryIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    slug = body.slug or slugify(body.name) or ("cat-" + secrets.token_hex(4))
    c = Category(slug=slug, **{k: v for k, v in body.model_dump().items() if k != "slug"})
    db.add(c)
    db.commit()
    db.refresh(c)
    return _cat_payload(c)

@app.put("/api/admin/categories/{cid}")
def admin_update_category(cid: int, body: CategoryIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    c = db.query(Category).filter(Category.id == cid).first()
    if not c:
        raise HTTPException(404, "دسته‌بندی یافت نشد")
    for k, v in body.model_dump().items():
        setattr(c, k, v)
    db.commit()
    return _cat_payload(c)

@app.delete("/api/admin/categories/{cid}")
def admin_delete_category(cid: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    c = db.query(Category).filter(Category.id == cid).first()
    if not c:
        raise HTTPException(404, "دسته‌بندی یافت نشد")
    db.delete(c)
    db.commit()
    return {"ok": True}

# ─── Admin – Orders ──────────────────────────────────────────────────────────
@app.get("/api/admin/orders")
def admin_orders(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return [_order_payload(o) for o in orders]

@app.put("/api/admin/orders/{oid}/status")
def admin_update_order_status(oid: int, body: dict, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.id == oid).first()
    if not o:
        raise HTTPException(404, "سفارش یافت نشد")
    if "order_status" in body:
        o.order_status = body["order_status"]
    if "payment_status" in body:
        o.payment_status = body["payment_status"]
    db.commit()
    return _order_payload(o)

# ─── Admin – Customers ───────────────────────────────────────────────────────
@app.get("/api/admin/customers")
def admin_customers(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_admin == False).order_by(User.created_at.desc()).all()
    return [{"id": u.id, "name": u.full_name, "email": u.email, "phone": u.phone,
             "created_at": u.created_at.isoformat()} for u in users]

# ─── Admin – Blog ────────────────────────────────────────────────────────────
@app.get("/api/admin/blog")
def admin_blog(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    posts = db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()
    return [{"id": p.id, "title": p.title, "slug": p.slug, "excerpt": p.excerpt,
             "cover_image": p.cover_image, "author": p.author, "category": p.category,
             "read_time": p.read_time, "is_published": p.is_published,
             "published_on": p.published_on, "created_at": p.created_at.isoformat()} for p in posts]

@app.post("/api/admin/blog")
def admin_create_post(body: BlogPostIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    slug = body.slug or slugify(body.title) or ("post-" + secrets.token_hex(4))
    p = BlogPost(slug=slug, **{k: v for k, v in body.model_dump().items() if k != "slug"})
    if not p.published_on:
        p.published_on = datetime.now().strftime("%Y-%m-%d")
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "slug": p.slug, "title": p.title}

@app.put("/api/admin/blog/{pid}")
def admin_update_post(pid: int, body: BlogPostIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    p = db.query(BlogPost).filter(BlogPost.id == pid).first()
    if not p:
        raise HTTPException(404, "مطلب یافت نشد")
    for k, v in body.model_dump().items():
        setattr(p, k, v)
    db.commit()
    return {"id": p.id, "slug": p.slug, "title": p.title}

@app.delete("/api/admin/blog/{pid}")
def admin_delete_post(pid: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    p = db.query(BlogPost).filter(BlogPost.id == pid).first()
    if not p:
        raise HTTPException(404)
    db.delete(p)
    db.commit()
    return {"ok": True}

# ─── Admin – FAQ ─────────────────────────────────────────────────────────────
@app.get("/api/admin/faq")
def admin_faq(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return [{"id": f.id, "question": f.question, "answer": f.answer, "display_order": f.display_order, "is_active": f.is_active}
            for f in db.query(Faq).order_by(Faq.display_order).all()]

@app.post("/api/admin/faq")
def admin_create_faq(body: FaqIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    f = Faq(**body.model_dump())
    db.add(f)
    db.commit()
    db.refresh(f)
    return {"id": f.id, "question": f.question, "answer": f.answer}

@app.put("/api/admin/faq/{fid}")
def admin_update_faq(fid: int, body: FaqIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    f = db.query(Faq).filter(Faq.id == fid).first()
    if not f:
        raise HTTPException(404)
    for k, v in body.model_dump().items():
        setattr(f, k, v)
    db.commit()
    return {"id": f.id}

@app.delete("/api/admin/faq/{fid}")
def admin_delete_faq(fid: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    f = db.query(Faq).filter(Faq.id == fid).first()
    if not f:
        raise HTTPException(404)
    db.delete(f)
    db.commit()
    return {"ok": True}

# ─── Admin – Coupons ─────────────────────────────────────────────────────────
@app.get("/api/admin/coupons")
def admin_coupons(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return [{"id": c.id, "code": c.code, "type": c.type, "value": c.value, "label": c.label,
             "min_order": c.min_order, "max_uses": c.max_uses, "used_count": c.used_count,
             "is_active": c.is_active, "expiry": c.expiry} for c in db.query(Coupon).all()]

@app.post("/api/admin/coupons")
def admin_create_coupon(body: CouponIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    body.code = body.code.upper()
    c = Coupon(**body.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "code": c.code}

@app.delete("/api/admin/coupons/{cid}")
def admin_delete_coupon(cid: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    c = db.query(Coupon).filter(Coupon.id == cid).first()
    if not c:
        raise HTTPException(404)
    db.delete(c)
    db.commit()
    return {"ok": True}

@app.patch("/api/admin/coupons/{cid}/toggle")
def admin_toggle_coupon(cid: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    c = db.query(Coupon).filter(Coupon.id == cid).first()
    if not c:
        raise HTTPException(404)
    c.is_active = not c.is_active
    db.commit()
    return {"is_active": c.is_active}

# ─── Admin – Navigation ──────────────────────────────────────────────────────
@app.get("/api/admin/navigation")
def admin_navigation(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    links = db.query(NavigationLink).order_by(NavigationLink.display_order).all()
    return [{"id": l.id, "label": l.label, "route": l.route, "placement": l.placement,
             "display_order": l.display_order, "is_active": l.is_active} for l in links]

@app.post("/api/admin/navigation")
def admin_create_nav(body: NavLinkIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    l = NavigationLink(**body.model_dump())
    db.add(l)
    db.commit()
    db.refresh(l)
    return {"id": l.id, "label": l.label, "route": l.route}

@app.put("/api/admin/navigation/{lid}")
def admin_update_nav(lid: int, body: NavLinkIn, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    l = db.query(NavigationLink).filter(NavigationLink.id == lid).first()
    if not l:
        raise HTTPException(404)
    for k, v in body.model_dump().items():
        setattr(l, k, v)
    db.commit()
    return {"id": l.id}

@app.delete("/api/admin/navigation/{lid}")
def admin_delete_nav(lid: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    l = db.query(NavigationLink).filter(NavigationLink.id == lid).first()
    if not l:
        raise HTTPException(404)
    db.delete(l)
    db.commit()
    return {"ok": True}

# ─── Admin – Site Settings ───────────────────────────────────────────────────
@app.put("/api/admin/site-settings")
def admin_update_settings(body: dict, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    for k, v in body.items():
        _set_setting(db, k, str(v))
    db.commit()
    return {"ok": True}

# ─── Admin – Returns ─────────────────────────────────────────────────────────
@app.get("/api/admin/returns")
def admin_returns(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    rets = db.query(ReturnRequest).order_by(ReturnRequest.created_at.desc()).all()
    return [{"id": r.id, "order_ref": r.order_ref, "reason": r.reason, "description": r.description,
             "status": r.status, "total_amount": r.total_amount, "admin_note": r.admin_note,
             "created_at": r.created_at.isoformat()} for r in rets]

@app.put("/api/admin/returns/{rid}/status")
def admin_update_return(rid: int, body: dict, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    r = db.query(ReturnRequest).filter(ReturnRequest.id == rid).first()
    if not r:
        raise HTTPException(404)
    r.status = body.get("status", r.status)
    r.admin_note = body.get("admin_note", r.admin_note)
    db.commit()
    return {"id": r.id, "status": r.status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
