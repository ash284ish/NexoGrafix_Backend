from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.blog_post import BlogPost


def seed_blog_posts():
    session: Session = SessionLocal()

    posts = [
        {
            "title": "Delivery playbook: quality gates & automation (18)",
            "slug": "delivery-playbook-quality-gates-automation-18",
            "excerpt": "Short, practical notes on improving delivery SLAs with automation, QA checkpoints, and structured workflows.",
        },
        {
            "title": "Building scalable QA workflows for publishing teams",
            "slug": "building-scalable-qa-workflows-publishing",
            "excerpt": "How structured QA processes help publishing teams scale without compromising quality.",
        },
        {
            "title": "Why automation is critical in modern content delivery",
            "slug": "why-automation-critical-modern-content-delivery",
            "excerpt": "Automation patterns that reduce manual effort and improve turnaround time in digital delivery.",
        },
        {
            "title": "From manuscript to market: digitization best practices",
            "slug": "manuscript-to-market-digitization-best-practices",
            "excerpt": "A practical guide to document digitization and structured content workflows.",
        },
        {
            "title": "Improving delivery SLAs with structured checkpoints",
            "slug": "improving-delivery-slas-structured-checkpoints",
            "excerpt": "How quality gates and checkpoints reduce rework and missed deadlines.",
        },
        {
            "title": "XML-first publishing: when and why it matters",
            "slug": "xml-first-publishing-when-and-why",
            "excerpt": "Understanding the long-term benefits of XML-first publishing pipelines.",
        },
        {
            "title": "Accessibility compliance in digital publishing",
            "slug": "accessibility-compliance-digital-publishing",
            "excerpt": "Key WCAG considerations and compliance strategies for modern publishers.",
        },
        {
            "title": "Reducing rework through better content planning",
            "slug": "reducing-rework-better-content-planning",
            "excerpt": "Why planning and structure matter more than speed in content operations.",
        },
        {
            "title": "Automating quality checks in large-scale publishing",
            "slug": "automating-quality-checks-large-scale-publishing",
            "excerpt": "Techniques to automate QA checks without losing editorial control.",
        },
        {
            "title": "Lessons learned from high-volume content delivery",
            "slug": "lessons-learned-high-volume-content-delivery",
            "excerpt": "Real-world insights from managing high-volume, multi-format content projects.",
        },
    ]

    content_html = """
    <article class="blog-content">

        <p>
            Contrary to popular belief, Lorem Ipsum is not simply random text.
            It has roots in classical Latin literature from 45 BC, making it over 2000 years old.
        </p>

        <p>
            Here you can write your real blog content later — abhi ke liye structure
            premium + clean hai. Tum bas data replace karte jaana.
        </p>

        <blockquote>
            <p>
                If you set your goals ridiculously high and it’s a failure,
                you will fail above everyone else’s success.
            </p>
            <footer>— Nelson Mandela</footer>
        </blockquote>

        <section class="image-text">
            <div class="image">
                <img src="https://cdn.example.com/blog-image-2.jpg" alt="Blog image" />
            </div>
            <div class="text">
                <p>
                    Is section me tum "image + content" type ka paragraph rakh sakte ho.
                    Desktop pe side-by-side rahega, mobile pe stack.
                </p>

                <p>
                    Delivery playbooks: QA gates, automation hooks, monitoring,
                    rollback plans — yaha explain kar sakte ho.
                </p>

                <div class="tags">
                    <span>Delivery</span>
                    <span>QA</span>
                    <span>Automation</span>
                </div>
            </div>
        </section>

        <figure>
            <img src="https://cdn.example.com/blog-image-3.jpg" alt="Blog image" />
        </figure>

        <p>
            Building a successful digital product is rarely about a single decision.
            It is a sequence of small, well-considered choices made consistently over time.
        </p>

        <p>
            Teams that invest in structured planning, transparent communication,
            and measurable milestones are far more likely to deliver products that scale.
        </p>

    </article>
    """

    for post_data in posts:
        exists = (
            session.query(BlogPost.id)
            .filter(BlogPost.slug == post_data["slug"])
            .first()
        )

        if exists:
            continue

        post = BlogPost(
            title=post_data["title"],
            slug=post_data["slug"],
            excerpt=post_data["excerpt"],
            content_html=content_html,
            cover_image_id=None,
            is_published=True,
        )

        session.add(post)

    session.commit()
    session.close()

    print("10 blog posts seeded successfully (existing skipped)")
