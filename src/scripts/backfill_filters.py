"""
Script to backfill topic and origin classifications for existing projects.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.client import get_client
from src.ai.classifier import ProjectClassifier

def backfill_classifications(limit=100):
    client = get_client()
    classifier = ProjectClassifier()
    
    # Fetch projects without topic or origin, or with 'other' topic
    response = client.table('projects').select('id, title, initiator, topic, origin') \
                     .or_('topic.is.null,topic.eq.other,origin.is.null') \
                     .limit(limit).execute()
    projects = response.data
    
    if not projects:
        print("No projects to backfill.")
        return

    print(f"Backfilling {len(projects)} projects...")
    
    for i, project in enumerate(projects):
        origin = classifier.determine_origin(project.get('initiator'))
        topic = classifier.classify_topic(project['title'], project.get('initiator'))
        
        print(f"[{i+1}/{len(projects)}] {project['title'][:40]}... -> {origin} | {topic}")
        
        client.table('projects').update({
            'origin': origin,
            'topic': topic
        }).eq('id', project['id']).execute()
        
        # Rate limiting to be nice to the API
        time.sleep(1)

if __name__ == "__main__":
    backfill_classifications()
