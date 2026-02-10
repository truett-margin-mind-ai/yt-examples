#!/usr/bin/env python3
"""
HubSpot Line Item Deletion Script

This script deletes line items created in January 2026.

Usage:
    1. Set environment variables:
       export HUBSPOT_ACCESS_TOKEN="your-token-here"
    
    2. Test on a single contact first (dry run):
       python fix_hubspot_line_items.py --test --contact-id 9407964769
    
    3. Execute deletion on a single contact:
       python fix_hubspot_line_items.py --execute --contact-id 9407964769
    
    4. Run on all affected records (after validation):
       python fix_hubspot_line_items.py --execute --all
"""

import os
import sys
import argparse
import logging
from datetime import datetime
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# HubSpot API configuration
HUBSPOT_API_BASE = "https://api.hubapi.com"


class HubSpotClient:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make a request to the HubSpot API."""
        url = f"{HUBSPOT_API_BASE}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            logger.error(f"Response: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            raise
    
    def get_line_items_for_contact(self, contact_id: str) -> list:
        """Get all line items associated with a contact via deals."""
        # First, get the deals associated with the contact
        endpoint = f"/crm/v3/objects/contacts/{contact_id}/associations/deals"
        
        try:
            response = self._request("GET", endpoint)
            deal_ids = [r["id"] for r in response.get("results", [])]
        except Exception as e:
            logger.warning(f"No deals found for contact {contact_id}: {e}")
            deal_ids = []
        
        # Get line items associated with those deals
        all_line_items = []
        for deal_id in deal_ids:
            endpoint = f"/crm/v3/objects/deals/{deal_id}/associations/line_items"
            try:
                response = self._request("GET", endpoint)
                line_item_ids = [r["id"] for r in response.get("results", [])]
                
                # Get full line item details
                for li_id in line_item_ids:
                    li_details = self.get_line_item(li_id)
                    li_details["_deal_id"] = deal_id
                    all_line_items.append(li_details)
            except Exception as e:
                logger.warning(f"Error getting line items for deal {deal_id}: {e}")
        
        return all_line_items
    
    def get_line_item(self, line_item_id: str) -> dict:
        """Get a single line item with all properties."""
        endpoint = f"/crm/v3/objects/line_items/{line_item_id}"
        params = "?properties=name,quantity,price,amount,description,createdate"
        return self._request("GET", endpoint + params)
    
    def search_line_items_by_date(self, start_date: str, end_date: str, limit: int = 100) -> list:
        """Search for line items created within a date range."""
        endpoint = "/crm/v3/objects/line_items/search"
        
        all_results = []
        after = None
        
        while True:
            data = {
                "filterGroups": [{
                    "filters": [
                        {
                            "propertyName": "createdate",
                            "operator": "GTE",
                            "value": start_date
                        },
                        {
                            "propertyName": "createdate",
                            "operator": "LTE", 
                            "value": end_date
                        }
                    ]
                }],
                "properties": ["name", "quantity", "price", "amount", "description", "createdate"],
                "limit": limit
            }
            
            if after:
                data["after"] = after
            
            response = self._request("POST", endpoint, data)
            results = response.get("results", [])
            all_results.extend(results)
            
            # Check for pagination
            paging = response.get("paging", {})
            after = paging.get("next", {}).get("after")
            
            if not after:
                break
        
        return all_results
    
    def delete_line_item(self, line_item_id: str) -> None:
        """Delete a line item."""
        endpoint = f"/crm/v3/objects/line_items/{line_item_id}"
        url = f"{HUBSPOT_API_BASE}{endpoint}"
        
        response = requests.delete(url, headers=self.headers, timeout=30)
        response.raise_for_status()


def parse_hubspot_date(date_str: str) -> datetime:
    """Parse a HubSpot date (either ISO format or milliseconds)."""
    if not date_str:
        return None
    
    # Try ISO format first (e.g., "2026-01-02T05:00:00Z")
    if isinstance(date_str, str) and "T" in date_str:
        try:
            # Handle ISO format with or without Z
            date_str = date_str.replace("Z", "+00:00")
            return datetime.fromisoformat(date_str.replace("+00:00", ""))
        except ValueError:
            pass
    
    # Try milliseconds timestamp
    try:
        timestamp_ms = int(date_str)
        return datetime.utcfromtimestamp(timestamp_ms / 1000)
    except (ValueError, TypeError):
        return None


def is_january_2026(date_str: str) -> bool:
    """Check if a date falls in January 2026."""
    dt = parse_hubspot_date(date_str)
    if not dt:
        return False
    return dt.year == 2026 and dt.month == 1


def format_date(date_str: str) -> str:
    """Format a HubSpot timestamp for display."""
    dt = parse_hubspot_date(date_str)
    if not dt:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def process_contact(client: HubSpotClient, contact_id: str, dry_run: bool = True):
    """Delete all January 2026 line items for a specific contact."""
    logger.info(f"\nProcessing contact: {contact_id}")
    logger.info("=" * 50)
    
    line_items = client.get_line_items_for_contact(contact_id)
    logger.info(f"Found {len(line_items)} total line items")
    
    jan_2026_items = []
    for li in line_items:
        create_date = li.get("properties", {}).get("createdate")
        if is_january_2026(create_date):
            jan_2026_items.append(li)
    
    logger.info(f"Found {len(jan_2026_items)} line items with January 2026 dates")
    
    if not jan_2026_items:
        logger.info("No line items to delete")
        return 0
    
    deleted_count = 0
    
    for li in jan_2026_items:
        props = li.get("properties", {})
        logger.info(f"\n  Line Item ID: {li['id']}")
        logger.info(f"    Name: {props.get('name', 'N/A')}")
        logger.info(f"    Amount: {props.get('amount', 'N/A')}")
        logger.info(f"    Create Date: {format_date(props.get('createdate'))}")
        
        if dry_run:
            logger.info("    [DRY RUN] Would delete this line item")
        else:
            try:
                client.delete_line_item(li["id"])
                logger.info("    DELETED")
                deleted_count += 1
            except Exception as e:
                logger.error(f"    Failed to delete: {e}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Summary: {'Would delete' if dry_run else 'Deleted'} {deleted_count if not dry_run else len(jan_2026_items)} line items")
    
    return deleted_count if not dry_run else len(jan_2026_items)


def process_all_january_2026(client: HubSpotClient, dry_run: bool = True):
    """Delete all line items created in January 2026."""
    logger.info("\nSearching for all line items created in January 2026...")
    logger.info("=" * 50)
    
    # January 2026 date range (in milliseconds)
    start_date = "1735689600000"  # 2026-01-01 00:00:00 UTC
    end_date = "1738367999000"    # 2026-01-31 23:59:59 UTC
    
    # Note: Above timestamps are actually for Jan 2025. Correct Jan 2026 timestamps:
    start_date = "1767225600000"  # 2026-01-01 00:00:00 UTC
    end_date = "1769903999000"    # 2026-01-31 23:59:59 UTC
    
    line_items = client.search_line_items_by_date(start_date, end_date)
    logger.info(f"Found {len(line_items)} line items in January 2026")
    
    if not line_items:
        logger.info("No line items to delete")
        return 0
    
    deleted_count = 0
    
    for li in line_items:
        props = li.get("properties", {})
        logger.info(f"\n  Line Item ID: {li['id']}")
        logger.info(f"    Name: {props.get('name', 'N/A')}")
        logger.info(f"    Amount: {props.get('amount', 'N/A')}")
        logger.info(f"    Create Date: {format_date(props.get('createdate'))}")
        
        if dry_run:
            logger.info("    [DRY RUN] Would delete this line item")
        else:
            try:
                client.delete_line_item(li["id"])
                logger.info("    DELETED")
                deleted_count += 1
            except Exception as e:
                logger.error(f"    Failed to delete: {e}")
    
    logger.info(f"\n{'='*50}")
    logger.info("FINAL SUMMARY")
    logger.info(f"  Total found: {len(line_items)}")
    logger.info(f"  {'Would delete' if dry_run else 'Deleted'}: {deleted_count if not dry_run else len(line_items)}")
    
    return deleted_count if not dry_run else len(line_items)


def main():
    parser = argparse.ArgumentParser(description="Delete HubSpot line items from January 2026")
    parser.add_argument("--test", action="store_true", 
                       help="Test mode: only show what would be deleted (dry run)")
    parser.add_argument("--execute", action="store_true",
                       help="Execute the deletions (required to make actual changes)")
    parser.add_argument("--contact-id", type=str,
                       help="Process only line items for a specific contact ID")
    parser.add_argument("--all", action="store_true",
                       help="Process all line items created in January 2026")
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.test and not args.execute:
        logger.error("Must specify either --test or --execute")
        sys.exit(1)
    
    if not args.contact_id and not args.all:
        logger.error("Must specify either --contact-id or --all")
        sys.exit(1)
    
    # Get API token
    access_token = os.environ.get("HUBSPOT_ACCESS_TOKEN")
    if not access_token:
        logger.error("HUBSPOT_ACCESS_TOKEN environment variable not set")
        logger.error("Run: export HUBSPOT_ACCESS_TOKEN='your-token-here'")
        sys.exit(1)
    
    dry_run = args.test
    
    if dry_run:
        logger.info("=" * 50)
        logger.info("DRY RUN MODE - No changes will be made")
        logger.info("=" * 50)
    else:
        logger.info("=" * 50)
        logger.info("EXECUTE MODE - Line items will be PERMANENTLY DELETED!")
        logger.info("=" * 50)
        
        # Confirmation prompt
        confirm = input("\nType 'DELETE' to confirm: ")
        if confirm != "DELETE":
            logger.info("Aborted.")
            sys.exit(0)
    
    client = HubSpotClient(access_token)
    
    if args.contact_id:
        process_contact(client, args.contact_id, dry_run=dry_run)
    elif args.all:
        process_all_january_2026(client, dry_run=dry_run)


if __name__ == "__main__":
    main()
