# Read persian help first


ENGLISH_HELP = """
Practice Exercise: Two‑Way Adapter (Coordinate Systems)

ENGLISH
-------

Goal
Implement a small system demonstrating a **two‑way Adapter pattern**
between two coordinate systems in 2D space.

The purpose of this exercise is to practice interface adaptation.
The math involved is intentionally simple. The focus is on design.

Coordinate Systems
------------------

1. Cartesian Coordinate System
   Represents a point using (x, y)

2. Polar Coordinate System
   Represents a point using (r, theta)

Where:
- r is the distance from the origin
- theta is the angle in radians

Both coordinate systems represent the same concept: a point in 2D space,
but they expose different interfaces and internal representations.

Core Requirement
----------------

Your system should allow objects from both coordinate systems to
interoperate through the use of an **Adapter**.

This should behave as a **two‑way adapter**, meaning that both
representations can work with each other when required.

Functional Requirements
-----------------------

Your design should support the following behaviors:

1) Coordinate Conversion

The system must allow conversion between the two coordinate systems.

Examples:

- Cartesian point → Polar representation
- Polar point → Cartesian representation


2) Translation (Moving a Point)

A point should be movable by applying a vector.

Important requirement:
The vector may be expressed in **either coordinate system**.

Example scenarios:

- A Cartesian point translated using a Cartesian vector
- A Polar point translated using a Polar vector
- A Polar point translated using a Cartesian vector
- A Cartesian point translated using a Polar vector


3) Basic Vector Support

Define simple vector objects for both coordinate systems:

- CartesianVector (dx, dy)
- PolarVector (magnitude, angle)

Vectors are only used to express movement.


Example Scenario
----------------

You might have:

    p = PolarPoint(r=5, theta=1.2)

And a translation vector defined in Cartesian coordinates:

    v = CartesianVector(dx=2, dy=1)

The system should allow:

    p.translate(v)

even though the point and the vector use different coordinate systems.


Design Objective
----------------

The goal is to practice designing a clean **Adapter-based interaction**
between two incompatible interfaces.

Avoid tightly coupling the coordinate implementations.


Focus of the Exercise
---------------------

Focus on:

- Interface adaptation
- Object interaction
- Practicing the Adapter pattern

Not on complex geometry.
"""


PERSIAN_HELP="""
نسخه فارسی (برای مرور سریع)

هدف تمرین
----------

یک سیستم ساده طراحی کن که **الگوی Adapter دوطرفه (Two‑Way Adapter)**
را بین دو دستگاه مختصات در فضای دوبعدی پیاده‌سازی کند.

هدف اصلی تمرین **طراحی و تطبیق اینترفیس‌ها** است، نه پیچیدگی ریاضی.


دستگاه‌های مختصات
-----------------

۱. دستگاه مختصات دکارتی
نمایش نقطه به صورت:

    (x, y)

۲. دستگاه مختصات قطبی
نمایش نقطه به صورت:

    (r, theta)

که در آن:

- r فاصله از مبدأ است
- theta زاویه بر حسب رادیان است


ایده اصلی
----------

هر دو دستگاه مختصات یک مفهوم مشترک را نمایش می‌دهند:
**یک نقطه در فضای دوبعدی**

اما:

- نمایش داخلی آنها متفاوت است
- اینترفیس‌های متفاوتی دارند


نیازمندی‌های عملکردی
--------------------

سیستم باید قابلیت‌های زیر را داشته باشد:


۱) تبدیل مختصات

امکان تبدیل بین دو دستگاه مختصات وجود داشته باشد:

- تبدیل Cartesian به Polar
- تبدیل Polar به Cartesian


۲) انتقال نقطه (Translation)

یک نقطه بتواند با استفاده از یک بردار جابجا شود.

نکته مهم:

بردار می‌تواند در **هر کدام از دستگاه‌های مختصات** تعریف شده باشد.


سناریوهای مورد انتظار

مثلاً:

- یک نقطه دکارتی با بردار دکارتی جابجا شود
- یک نقطه قطبی با بردار قطبی جابجا شود
- یک نقطه قطبی با بردار دکارتی جابجا شود
- یک نقطه دکارتی با بردار قطبی جابجا شود


۳) بردارها

دو نوع بردار ساده تعریف کن:

- CartesianVector(dx, dy)
- PolarVector(magnitude, angle)

بردار فقط برای **جابجا کردن نقطه** استفاده می‌شود.


هدف طراحی
---------

هدف تمرین این است که با استفاده از **Adapter**
بتوانی این دو سیستم ناسازگار را طوری طراحی کنی که با هم کار کنند.

سعی کن وابستگی مستقیم بین پیاده‌سازی‌های مختصات ایجاد نکنی.


تمرکز تمرین
-----------

تمرکز این تمرین روی موارد زیر است:

- Adapter Pattern
- تطبیق اینترفیس‌ها
- تعامل بین آبجکت‌ها

نه روی ریاضیات پیچیده.
"""


print(PERSIAN_HELP)
