from datetime import datetime, timedelta
from app.repos.deal import DealRepo
from app.core.cache import get_cache, set_cache


class AnalyticsService:
    def __init__(self, db, org_id):
        self.db = db
        self.org_id = org_id
        self.repo = DealRepo(db)

    def get_summary(self):
        cache_key = f"analytics_summary_{self.org_id}"
        cached = get_cache(cache_key)
        if cached:
            return cached

        deals = self.repo.get_for_org(self.org_id)

        status_counts = {}
        status_amounts = {}
        won_amounts = []

        for deal in deals:
            status_counts[deal.status] = status_counts.get(deal.status, 0) + 1
            status_amounts[deal.status] = status_amounts.get(deal.status, 0) + float(deal.amount)
            if deal.status == 'won':
                won_amounts.append(float(deal.amount))

        recent = datetime.now() - timedelta(days=30)
        new_count = sum(1 for d in deals if d.created_at >= recent)

        avg_won = sum(won_amounts) / len(won_amounts) if won_amounts else 0

        result = {
            "status_counts": status_counts,
            "status_amounts": status_amounts,
            "avg_won_amount": round(avg_won, 2),
            "new_last_30_days": new_count
        }

        set_cache(cache_key, result, ttl=60)
        return result

    def get_funnel(self):
        cache_key = f"analytics_funnel_{self.org_id}"
        cached = get_cache(cache_key)
        if cached:
            return cached

        deals = self.repo.get_for_org(self.org_id)

        stages = ["qualification", "proposal", "negotiation", "closed"]
        stage_counts = {stage: 0 for stage in stages}

        for deal in deals:
            if deal.stage in stage_counts:
                stage_counts[deal.stage] += 1

        funnel = []
        prev_count = None
        for stage in stages:
            count = stage_counts[stage]
            conversion = 0
            if count > 0:
                conversion = round((prev_count / count * 100), 2) if prev_count and count else 0
            funnel.append({
                "stage": stage,
                "count": count,
                "conversion_from_previous": conversion
            })
            prev_count = count

        set_cache(cache_key, funnel, ttl=60)
        return funnel