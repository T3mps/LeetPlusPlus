#!/usr/bin/env python3
"""
Metadata Updater for LeetPlusPlus
Fetches problem list from LeetCode API and creates/updates metadata.json
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from common import ColorPrinter, APIServerManager, MetadataManager, HTTPClient, Fore, Style
from config import API_BASE_URL, METADATA_FILE, BATCH_FETCH_LIMIT
from ui_style import UIStyle

class MetadataUpdater:
    def __init__(self):
        self.api_base = API_BASE_URL
        self.api_manager = APIServerManager(self.api_base)
        self.metadata_manager = MetadataManager(METADATA_FILE)
        self.http_client = HTTPClient()
        
    def fetch_all_problems(self):
        """Fetch all problems from the API"""
        ColorPrinter.info("Fetching problem list from API...")
        all_problems = []
        skip = 0
        limit = BATCH_FETCH_LIMIT
        
        while True:
            data = self.http_client.get_with_params(
                f"{self.api_base}/problems",
                {"limit": str(limit), "skip": str(skip)}
            )
            
            if not data:
                break
            
            # The API returns an object with problemsetQuestionList
            if 'problemsetQuestionList' in data:
                problems = data['problemsetQuestionList']
                if not problems:
                    break
                all_problems.extend(problems)
                skip += limit
                # Show count instead of progress bar since we don't know total
                print(f"\r  Fetched {len(all_problems)} problems...", end='', flush=True)
            else:
                # Might be a different format
                if isinstance(data, list):
                    if not data:
                        break
                    all_problems.extend(data)
                    skip += limit
                    # Show count instead of progress bar since we don't know total
                    print(f"\r  Fetched {len(all_problems)} problems...", end='', flush=True)
                else:
                    ColorPrinter.warning("Unexpected API response format")
                    break
        
        print()  # New line after progress
        return all_problems
    
    def build_metadata(self, problems):
        """Build metadata dictionary from problem list"""
        ColorPrinter.info("Building metadata...")
        
        # Start with fresh metadata - complete override
        metadata = {}
        
        # Process all problems
        total_processed = 0
        skipped_paid = 0
        
        for problem in problems:
            # Extract problem number and other details
            problem_id = str(problem.get('questionFrontendId', ''))
            if not problem_id or problem_id == '0':
                continue
            
            # Skip paid-only problems
            if problem.get('isPaidOnly', False):
                skipped_paid += 1
                continue
            
            metadata[problem_id] = {
                'titleSlug': problem.get('titleSlug', ''),
                'title': problem.get('title', ''),
                'difficulty': problem.get('difficulty', 'Medium'),
                'isPaidOnly': False,  # We're only storing free problems
                'topicTags': [tag.get('name', '') for tag in problem.get('topicTags', [])]
                         if isinstance(problem.get('topicTags'), list) else [],
                'acRate': problem.get('acRate', None),  # Acceptance rate if available
            }
            
            total_processed += 1
        
        print(f"  Processed: {total_processed} problems")
        print(f"  Skipped: {skipped_paid} paid-only problems")
        print(f"  Total: {len(metadata)} problems (free only)")
        
        return metadata
    
    def save_metadata(self, metadata):
        """Save metadata to file"""
        ColorPrinter.info("Saving metadata...")
        
        if self.metadata_manager.save(metadata):
            ColorPrinter.success(f"Metadata saved successfully to: {METADATA_FILE}")
        else:
            ColorPrinter.error("Failed to save metadata")
    
    def _check_and_start_api(self):
        """Check if API is running and start it if needed"""
        return self.api_manager.ensure_running()
    
    def run(self):
        """Main update process"""
        print(UIStyle.header("LeetPlusPlus Metadata Updater", "Fetching problem data from LeetCode API"))
        
        # Check if API is running and auto-start if needed
        if not self._check_and_start_api():
            return 1
        
        # Fetch all problems
        problems = self.fetch_all_problems()
        if problems is None:
            return 1
        
        if not problems:
            ColorPrinter.error("No problems fetched!")
            return 1
        
        # Build and save metadata
        metadata = self.build_metadata(problems)
        self.save_metadata(metadata)
        
        # Show some statistics
        print(UIStyle.section_header("Statistics"))
        difficulties = {'Easy': 0, 'Medium': 0, 'Hard': 0}
        
        for info in metadata.values():
            difficulties[info.get('difficulty', 'Medium')] += 1
        
        # Display with color coding
        print(f"  {Fore.GREEN}Easy{Style.RESET_ALL}:   {difficulties['Easy']:>4}")
        print(f"  {Fore.YELLOW}Medium{Style.RESET_ALL}: {difficulties['Medium']:>4}")
        print(f"  {Fore.RED}Hard{Style.RESET_ALL}:   {difficulties['Hard']:>4}")
        print(f"  {Fore.CYAN}Total{Style.RESET_ALL}:  {len(metadata):>4} (free problems only)")
        
        print(UIStyle.footer("Metadata update completed successfully!"))
        
        return 0

def main():
    updater = MetadataUpdater()
    sys.exit(updater.run())

if __name__ == "__main__":
    main()