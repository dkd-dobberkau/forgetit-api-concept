import json
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt
import numpy as np
from textwrap import dedent

class ProgressiveCondensation:
    """
    Simulates how digital resources would undergo progressive condensation 
    based on the ForgetIT project's concepts.
    """
    
    def __init__(self):
        self.resources = []
        self.condensation_snapshots = {}
        self.time_now = datetime.now()
    
    def create_sample_resource(self, title, content_type, content, importance=0.5, initial_mb=0.9):
        """Create a sample resource with initial values"""
        resource = {
            "id": len(self.resources) + 1,
            "title": title,
            "content_type": content_type,
            "content": content,
            "created_at": self.time_now - timedelta(days=random.randint(30, 365)),
            "last_accessed": self.time_now,
            "access_count": 1,
            "memory_buoyancy": initial_mb,
            "preservation_value": importance,
            "condensation_level": 0,  # 0 = original, 1-5 increasing condensation
            "views_history": []
        }
        self.resources.append(resource)
        return resource["id"]
    
    def simulate_time_passing(self, days):
        """Simulate time passing and memory buoyancy declining"""
        for resource in self.resources:
            # Decay memory buoyancy over time
            # The decay rate depends on the resource type and importance
            base_decay_rate = 0.1
            
            # Adjust decay rate based on content type
            type_factors = {
                "document": 1.0,
                "image": 0.8,     # Photos tend to remain more memorable
                "email": 1.2,     # Emails tend to be forgotten faster
                "code": 0.9,      # Code has slightly better retention
                "note": 1.3       # Notes are forgotten quickly
            }
            
            # Adjust decay rate based on preservation value
            preservation_factor = 1.0 - (resource["preservation_value"] * 0.5)
            
            # Calculate final decay rate
            decay_rate = base_decay_rate * type_factors.get(resource["content_type"], 1.0) * preservation_factor
            
            # Apply decay
            days_since_access = (self.time_now - resource["last_accessed"]).days + days
            resource["memory_buoyancy"] *= (1 - (decay_rate * days / 365))
            
            # Ensure memory buoyancy stays within bounds
            resource["memory_buoyancy"] = max(0.01, min(0.99, resource["memory_buoyancy"]))
            
            # Update condensation level based on memory buoyancy
            if resource["memory_buoyancy"] > 0.8:
                resource["condensation_level"] = 0  # Original
            elif resource["memory_buoyancy"] > 0.6:
                resource["condensation_level"] = 1  # Light condensation
            elif resource["memory_buoyancy"] > 0.4:
                resource["condensation_level"] = 2  # Medium condensation
            elif resource["memory_buoyancy"] > 0.2:
                resource["condensation_level"] = 3  # Heavy condensation
            elif resource["memory_buoyancy"] > 0.1:
                resource["condensation_level"] = 4  # Severe condensation
            else:
                resource["condensation_level"] = 5  # Maximum condensation
        
        # Advance current time
        self.time_now += timedelta(days=days)
    
    def simulate_resource_access(self, resource_id):
        """Simulate accessing a resource, which increases its memory buoyancy"""
        resource = next((r for r in self.resources if r["id"] == resource_id), None)
        if resource:
            # Record access time
            resource["last_accessed"] = self.time_now
            resource["access_count"] += 1
            
            # Boost memory buoyancy (but with diminishing returns for repeated access)
            boost = 0.2 * (1 - resource["memory_buoyancy"])
            resource["memory_buoyancy"] = min(0.99, resource["memory_buoyancy"] + boost)
            
            # Record for visualization
            resource["views_history"].append({
                "date": self.time_now,
                "memory_buoyancy": resource["memory_buoyancy"]
            })
            
            # Update condensation level
            if resource["memory_buoyancy"] > 0.8:
                resource["condensation_level"] = 0
    
    def get_condensed_content(self, resource_id):
        """Get the condensed representation of a resource based on its current condensation level"""
        resource = next((r for r in self.resources if r["id"] == resource_id), None)
        if not resource:
            return None
        
        content = resource["content"]
        content_type = resource["content_type"]
        level = resource["condensation_level"]
        
        # Different condensation strategies for different content types
        if content_type == "document":
            return self._condense_document(content, level)
        elif content_type == "image":
            return self._condense_image(content, level)
        elif content_type == "email":
            return self._condense_email(content, level)
        elif content_type == "code":
            return self._condense_code(content, level)
        elif content_type == "note":
            return self._condense_note(content, level)
        else:
            return content  # No condensation for unknown types
    
    def _condense_document(self, content, level):
        """Condense a document based on condensation level"""
        if level == 0:
            return content  # Full content
        
        lines = content.split("\n")
        word_count = len(content.split())
        
        if level == 1:
            # Light condensation: Keep ~80% of content, focus on reducing verbosity
            return self._extract_key_sentences(content, int(word_count * 0.8))
        elif level == 2:
            # Medium condensation: Keep ~50% of content, summarize main points
            return self._extract_key_sentences(content, int(word_count * 0.5))
        elif level == 3:
            # Heavy condensation: Keep ~25% of content, just the essential points
            return self._extract_key_sentences(content, int(word_count * 0.25))
        elif level == 4:
            # Severe condensation: Key sentences only (10%)
            return self._extract_key_sentences(content, int(word_count * 0.1))
        else:  # level == 5
            # Maximum condensation: Title + metadata only
            return f"[Document summary - {word_count} words]"
    
    def _condense_image(self, content, level):
        """Simulate condensing an image"""
        # For images, condensation might mean:
        # - Reducing resolution
        # - Converting to grayscale
        # - Showing only thumbnails or metadata
        if level == 0:
            return content  # Full resolution image
        elif level == 1:
            return "[Image: 80% resolution]"
        elif level == 2:
            return "[Image: 50% resolution]"
        elif level == 3:
            return "[Image: thumbnail]"
        elif level == 4:
            return "[Image: metadata only]"
        else:  # level == 5
            return "[Image reference]"
    
    def _condense_email(self, content, level):
        """Condense an email based on condensation level"""
        # For emails, we might keep the subject and recipients but condense the body
        if level == 0:
            return content
        
        lines = content.split("\n")
        subject_line = next((line for line in lines if line.startswith("Subject:")), "")
        from_line = next((line for line in lines if line.startswith("From:")), "")
        
        if level == 1:
            # Keep header and ~75% of body
            return f"{from_line}\n{subject_line}\n\n{self._extract_key_sentences(' '.join(lines[3:]), int(len(' '.join(lines[3:])) * 0.75))}"
        elif level == 2:
            # Keep header and ~50% of body
            return f"{from_line}\n{subject_line}\n\n{self._extract_key_sentences(' '.join(lines[3:]), int(len(' '.join(lines[3:])) * 0.5))}"
        elif level == 3:
            # Keep header and a few key sentences
            return f"{from_line}\n{subject_line}\n\n{self._extract_key_sentences(' '.join(lines[3:]), int(len(' '.join(lines[3:])) * 0.25))}"
        elif level == 4:
            # Keep only header and first sentence
            return f"{from_line}\n{subject_line}\n\n[Email body condensed]"
        else:  # level == 5
            # Just the subject
            return f"{subject_line} [Email reference]"
    
    def _condense_code(self, content, level):
        """Condense code based on condensation level"""
        if level == 0:
            return content
        
        lines = content.split("\n")
        # Look for function/class definitions as key structural elements
        definitions = [i for i, line in enumerate(lines) if line.strip().startswith(("def ", "class "))]
        
        if level == 1:
            # Keep all code but remove detailed comments
            return "\n".join([l for l in lines if not l.strip().startswith("#") or len(l.strip()) < 3])
        elif level == 2:
            # Keep function definitions and key sections
            if not definitions:
                return "\n".join(lines[:max(5, len(lines)//2)])
            else:
                preserved_lines = []
                for i in definitions:
                    # Add function definition and a few lines after it
                    preserved_lines.extend(lines[i:min(i+5, len(lines))])
                return "\n".join(preserved_lines)
        elif level == 3:
            # Just function/class signatures
            if not definitions:
                return lines[0] if lines else "[Code excerpt]"
            else:
                return "\n".join([lines[i] + " ..." for i in definitions])
        elif level == 4:
            # Just a summary of what the code contains
            func_count = len([l for l in lines if l.strip().startswith("def ")])
            class_count = len([l for l in lines if l.strip().startswith("class ")])
            return f"[Code: {len(lines)} lines, {func_count} functions, {class_count} classes]"
        else:  # level == 5
            return "[Code reference]"
    
    def _condense_note(self, content, level):
        """Condense a note based on condensation level"""
        if level == 0:
            return content
        
        words = content.split()
        
        if level == 1:
            return " ".join(words[:int(len(words) * 0.8)])
        elif level == 2:
            return " ".join(words[:int(len(words) * 0.6)])
        elif level == 3:
            return " ".join(words[:int(len(words) * 0.4)])
        elif level == 4:
            return " ".join(words[:min(10, len(words))])
        else:  # level == 5
            return "[Note reference]"
    
    def _extract_key_sentences(self, text, target_length):
        """Simple extractive summarization - in a real system this would be more sophisticated"""
        sentences = text.replace("\n", " ").split(". ")
        if target_length >= len(text):
            return text
        
        # In a real system, we would use NLP to extract the most important sentences
        # For this demo, we'll just take sentences from the beginning, middle, and end
        if len(sentences) <= 3:
            return text
        
        sentences_to_keep = min(len(sentences), max(1, int(len(sentences) * target_length / len(text))))
        
        # Take sentences from beginning, middle and end
        if sentences_to_keep >= len(sentences):
            return ". ".join(sentences)
        elif sentences_to_keep == 1:
            return sentences[0] + "."
        else:
            step = len(sentences) // sentences_to_keep
            selected_indices = [i for i in range(0, len(sentences), step)][:sentences_to_keep]
            return ". ".join([sentences[i] for i in selected_indices]) + "."
    
    def capture_condensation_snapshot(self, resource_id):
        """Capture a snapshot of the current condensation state for visualization"""
        resource = next((r for r in self.resources if r["id"] == resource_id), None)
        if not resource:
            return
        
        if resource_id not in self.condensation_snapshots:
            self.condensation_snapshots[resource_id] = []
        
        self.condensation_snapshots[resource_id].append({
            "date": self.time_now,
            "memory_buoyancy": resource["memory_buoyancy"],
            "condensation_level": resource["condensation_level"],
            "content": self.get_condensed_content(resource_id)
        })
    
    def visualize_progressive_condensation(self, resource_id):
        """Create a visualization of how condensation progresses over time"""
        resource = next((r for r in self.resources if r["id"] == resource_id), None)
        if not resource or resource_id not in self.condensation_snapshots:
            print(f"No visualization data for resource {resource_id}")
            return
        
        snapshots = self.condensation_snapshots[resource_id]
        
        # Extract data for plotting
        dates = [s["date"] for s in snapshots]
        memory_buoyancy = [s["memory_buoyancy"] for s in snapshots]
        condensation_levels = [s["condensation_level"] for s in snapshots]
        
        # Convert dates to days from start for easier plotting
        start_date = dates[0]
        days = [(d - start_date).days for d in dates]
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Plot memory buoyancy
        ax1.plot(days, memory_buoyancy, 'b-', marker='o', markersize=8)
        ax1.set_ylabel('Memory Buoyancy')
        ax1.set_title(f'Progressive Condensation for "{resource["title"]}"')
        ax1.grid(True)
        ax1.set_ylim(0, 1)
        
        # Plot condensation level (inverted scale)
        ax2.plot(days, condensation_levels, 'r-', marker='s', markersize=8)
        ax2.set_ylabel('Condensation Level')
        ax2.set_xlabel('Days from Start')
        ax2.set_ylim(5, 0)  # Inverted scale (0 = original, 5 = max condensation)
        ax2.set_yticks(range(6))
        ax2.set_yticklabels(['Original', 'Light', 'Medium', 'Heavy', 'Severe', 'Minimal'])
        ax2.grid(True)
        
        # Add annotations for access events
        if resource["views_history"]:
            view_days = [(v["date"] - start_date).days for v in resource["views_history"]]
            view_mb = [v["memory_buoyancy"] for v in resource["views_history"]]
            ax1.plot(view_days, view_mb, 'go', markersize=10)
            for i, day in enumerate(view_days):
                ax1.annotate(f'Access', xy=(day, view_mb[i]), 
                            xytext=(day+1, view_mb[i]+0.05),
                            arrowprops=dict(facecolor='green', shrink=0.05))
        
        plt.tight_layout()
        plt.savefig(f"progressive_condensation_{resource_id}.png")
        plt.close()
        
        # Print the content at different condensation levels
        print(f"\nContent Evolution for: {resource['title']}")
        print("=" * 80)
        for i, snapshot in enumerate(snapshots):
            print(f"\nDay {days[i]} - Memory Buoyancy: {snapshot['memory_buoyancy']:.2f} - Level: {snapshot['condensation_level']}")
            print("-" * 80)
            print(snapshot["content"])
        
        return f"Visualization saved as progressive_condensation_{resource_id}.png"

# Demonstration of progressive condensation
def demonstrate_progressive_condensation():
    sim = ProgressiveCondensation()
    
    # Create sample resources
    document_id = sim.create_sample_resource(
        "Project Proposal: AI-Powered Data Analysis",
        "document",
        dedent("""
        Project Proposal: AI-Powered Data Analysis
        
        Executive Summary:
        This proposal outlines a comprehensive approach to implementing artificial intelligence algorithms for data analysis within our organization. The project aims to reduce manual data processing by 75% while increasing analytical accuracy by at least 35%.
        
        Background:
        Currently, our data analysis processes rely heavily on manual extraction and interpretation, leading to inefficiencies and potential inaccuracies. Market research indicates that similar organizations have achieved significant operational improvements through AI implementation.
        
        Methodology:
        1. Data Collection and Preparation
        2. Algorithm Selection and Customization
        3. Integration with Existing Systems
        4. Testing and Validation
        5. Staff Training and Deployment
        
        Timeline:
        The project is estimated to take 6 months from initiation to full deployment, with key milestones at months 2, 4, and 5.
        
        Budget:
        Total estimated cost: $425,000, including software licensing, consulting services, and internal resource allocation.
        
        Expected Benefits:
        - Reduced processing time from 4.2 days to under 1 day
        - Improved accuracy in predictive analytics
        - Enhanced reporting capabilities
        - Potential annual savings of $380,000
        
        Conclusion:
        This investment in AI-powered data analysis represents a strategic opportunity to enhance our operational efficiency while positioning us for future growth and innovation in the data-driven marketplace.
        """),
        importance=0.85,
        initial_mb=0.95
    )
    
    # Add more resource types
    email_id = sim.create_sample_resource(
        "Meeting Follow-up: Quarterly Planning",
        "email",
        dedent("""
        From: manager@company.com
        To: team@company.com
        Subject: Follow-up from Quarterly Planning Meeting
        
        Team,
        
        Thanks for your participation in yesterday's quarterly planning session. I wanted to summarize the key decisions and action items:
        
        1. We will prioritize the customer portal redesign for Q3, with a target launch date of September 15.
        
        2. Marketing campaign for the new product line will begin in August, coordinated by Sarah.
        
        3. Budget adjustments have been approved - department heads will receive updated figures by Friday.
        
        4. The office relocation timeline has been pushed back by one month due to construction delays.
        
        5. Next all-hands meeting is scheduled for July 12 at 10 AM.
        
        Please review the attached presentation for additional details. Let me know if you have any questions.
        
        Regards,
        Manager
        """),
        importance=0.65,
        initial_mb=0.9
    )
    
    code_id = sim.create_sample_resource(
        "Data Processing Utility Function",
        "code",
        dedent("""
        def process_data_batch(data_list, normalize=True, filter_outliers=False):
            \"\"\"
            Process a batch of data points applying normalization and outlier filtering.
            
            Parameters:
            - data_list (list): List of numeric data points to process
            - normalize (bool): Whether to normalize the data to 0-1 range
            - filter_outliers (bool): Whether to remove statistical outliers
            
            Returns:
            - Processed data as numpy array
            \"\"\"
            import numpy as np
            
            # Convert to numpy array for processing
            data_array = np.array(data_list, dtype=float)
            
            # Remove NaN values
            data_array = data_array[~np.isnan(data_array)]
            
            if filter_outliers and len(data_array) > 10:
                # Remove outliers (values more than 3 std from mean)
                mean = np.mean(data_array)
                std = np.std(data_array)
                data_array = data_array[abs(data_array - mean) <= 3 * std]
            
            if normalize and len(data_array) > 0:
                # Normalize to 0-1 range
                min_val = np.min(data_array)
                max_val = np.max(data_array)
                if max_val > min_val:  # Avoid division by zero
                    data_array = (data_array - min_val) / (max_val - min_val)
            
            return data_array
        """),
        importance=0.75,
        initial_mb=0.85
    )
    
    note_id = sim.create_sample_resource(
        "Office Supplies to Order",
        "note",
        "Printer paper (5 reams), Stapler, Blue pens (box of 12), Sticky notes (assorted colors), Whiteboard markers, Hand sanitizer, Coffee pods for meeting room",
        importance=0.3,
        initial_mb=0.8
    )
    
    # Capture initial state
    for resource_id in [document_id, email_id, code_id, note_id]:
        sim.capture_condensation_snapshot(resource_id)
    
    # Simulate 30 days passing
    sim.simulate_time_passing(30)
    
    # Access code resource (simulating continued use)
    sim.simulate_resource_access(code_id)
    
    # Capture state after 30 days
    for resource_id in [document_id, email_id, code_id, note_id]:
        sim.capture_condensation_snapshot(resource_id)
    
    # Simulate another 60 days passing
    sim.simulate_time_passing(60)
    
    # Access document (simulating revisiting an important document)
    sim.simulate_resource_access(document_id)
    
    # Capture state after 90 days
    for resource_id in [document_id, email_id, code_id, note_id]:
        sim.capture_condensation_snapshot(resource_id)
    
    # Simulate another 90 days
    sim.simulate_time_passing(90)
    
    # Capture state after 180 days
    for resource_id in [document_id, email_id, code_id, note_id]:
        sim.capture_condensation_snapshot(resource_id)
    
    # Simulate another 180 days
    sim.simulate_time_passing(180)
    
    # Access code again (simulating revisiting after long time)
    sim.simulate_resource_access(code_id)
    
    # Capture final state after 1 year
    for resource_id in [document_id, email_id, code_id, note_id]:
        sim.capture_condensation_snapshot(resource_id)
    
    # Visualize the progression for the document
    print(sim.visualize_progressive_condensation(document_id))
    print("\n" + "=" * 80 + "\n")
    
    # Visualize for other resource types
    print(sim.visualize_progressive_condensation(email_id))
    print("\n" + "=" * 80 + "\n")
    
    print(sim.visualize_progressive_condensation(code_id))
    print("\n" + "=" * 80 + "\n")
    
    print(sim.visualize_progressive_condensation(note_id))

if __name__ == "__main__":
    demonstrate_progressive_condensation()
