"""
AI Failure Analyzer - Uses GPT-4o to analyze Robot Framework test failures
and suggest intelligent fixes based on error messages and context.
"""

import os
import json
import sys
from robot.api import ExecutionResult, ResultVisitor
from robot.result.model import TestCase
import requests
from datetime import datetime
import urllib3

# Disable SSL warnings for internal network
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AIFailureAnalyzer:
    """Analyzes Robot Framework test failures using AI and suggests fixes."""
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        """Initialize the AI Failure Analyzer with Walmart AI Gateway config."""
        # Load config from ai_config.yaml or environment
        self.api_url = "https://wmtllmgateway.stage.walmart.com/wmtllmgateway/openai/deployments/gpt-4o/chat/completions"
        self.api_version = "2024-02-15-preview"
        
        # JWT token from config.py
        try:
            sys.path.insert(0, os.path.dirname(__file__))
            from config import AI_CONFIG
            self.jwt_token = AI_CONFIG['api_key']
        except ImportError:
            raise Exception("Could not import AI_CONFIG from config.py")
    
    def analyze_failure(self, test_name, error_message, test_steps=None):
        """
        Analyze a single test failure using AI.
        
        Args:
            test_name: Name of the failed test
            error_message: Error message from Robot Framework
            test_steps: Optional list of test steps for context
            
        Returns:
            Dictionary with AI analysis and suggestions
        """
        # Create AI prompt
        prompt = self._create_analysis_prompt(test_name, error_message, test_steps)
        
        # Call GPT-4o
        response = self._call_ai_api(prompt)
        
        return {
            'test_name': test_name,
            'error_message': error_message,
            'ai_analysis': response,
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_output_xml(self, output_xml_path):
        """
        Analyze all failures in a Robot Framework output.xml file.
        
        Args:
            output_xml_path: Path to output.xml file
            
        Returns:
            Dictionary with analysis results for all failed tests
        """
        result = ExecutionResult(output_xml_path)
        
        failures = []
        visitor = FailureCollector(failures)
        result.visit(visitor)
        
        print(f"\n{'='*80}")
        print(f"AI FAILURE ANALYSIS REPORT")
        print(f"{'='*80}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Output File: {output_xml_path}")
        print(f"Total Tests: {result.statistics.total.total}")
        print(f"Failed Tests: {result.statistics.total.failed}")
        print(f"{'='*80}\n")
        
        analyses = []
        for idx, failure in enumerate(failures, 1):
            print(f"\n{'─'*80}")
            print(f"FAILURE #{idx}: {failure['test_name']}")
            print(f"{'─'*80}")
            print(f"\n📋 ERROR MESSAGE:")
            print(f"{failure['error_message']}\n")
            
            analysis = self.analyze_failure(
                failure['test_name'],
                failure['error_message'],
                failure.get('steps')
            )
            
            print(f"🤖 AI ANALYSIS:")
            print(f"{analysis['ai_analysis']}\n")
            
            analyses.append(analysis)
        
        print(f"\n{'='*80}")
        print(f"Analysis complete. Total failures analyzed: {len(analyses)}")
        print(f"{'='*80}\n")
        
        return {
            'total_tests': result.statistics.total.total,
            'failed_tests': result.statistics.total.failed,
            'passed_tests': result.statistics.total.passed,
            'analyses': analyses,
            'generated_at': datetime.now().isoformat()
        }
    
    def _create_analysis_prompt(self, test_name, error_message, test_steps=None):
        """Create the AI prompt for failure analysis."""
        prompt_parts = [
            "You are an expert QA automation engineer analyzing Robot Framework test failures.",
            "",
            f"TEST NAME: {test_name}",
            "",
            f"ERROR MESSAGE:",
            error_message,
            ""
        ]
        
        if test_steps:
            prompt_parts.extend([
                "TEST STEPS:",
                *test_steps,
                ""
            ])
        
        prompt_parts.extend([
            "Please analyze this failure and provide:",
            "1. Root Cause: What went wrong and why",
            "2. Fix Suggestion: Specific code changes to fix the issue",
            "3. Prevention: How to prevent similar issues in the future",
            "",
            "Be concise, specific, and actionable. Focus on Robot Framework and Selenium best practices."
        ])
        
        return "\n".join(prompt_parts)
    
    def _call_ai_api(self, prompt, max_tokens=500, temperature=0.3):
        """Call the Walmart AI Gateway GPT-4o API."""
        # Prepare request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jwt_token}',
            'api-key': self.jwt_token
        }
        
        # Create content in multimodal format
        content = [{'type': 'text', 'text': prompt}]
        
        payload = {
            'messages': [
                {'role': 'user', 'content': content}
            ],
            'max_tokens': int(max_tokens),
            'temperature': float(temperature)
        }
        
        # Make API call
        try:
            response = requests.post(
                f"{self.api_url}?api-version={self.api_version}",
                headers=headers,
                json=payload,
                timeout=30,
                verify=False  # Disable SSL verification for internal Walmart network
            )
            
            if response.status_code == 200:
                response_json = response.json()
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    return response_json['choices'][0]['message']['content']
                else:
                    return f"Error: No response from AI (status {response.status_code})"
            else:
                return f"Error: API returned status {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error calling AI API: {str(e)}"
    
    def generate_analysis_report(self, output_xml_path, report_path=None):
        """
        Generate a detailed HTML report with AI analysis.
        
        Args:
            output_xml_path: Path to output.xml file
            report_path: Optional path for the report (default: ai-analysis-report.html)
            
        Returns:
            Path to generated report
        """
        if report_path is None:
            report_dir = os.path.dirname(output_xml_path)
            report_path = os.path.join(report_dir, 'ai-analysis-report.html')
        
        analysis_data = self.analyze_output_xml(output_xml_path)
        
        # Generate HTML report
        html = self._generate_html_report(analysis_data)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n📊 AI Analysis Report generated: {report_path}")
        return report_path
    
    def _generate_html_report(self, analysis_data):
        """Generate HTML report from analysis data."""
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <title>AI Failure Analysis Report</title>',
            '    <style>',
            '        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }',
            '        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }',
            '        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }',
            '        h2 { color: #34495e; margin-top: 30px; }',
            '        .summary { background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }',
            '        .summary-stat { display: inline-block; margin: 10px 20px; }',
            '        .summary-stat .label { font-weight: bold; color: #7f8c8d; }',
            '        .summary-stat .value { font-size: 24px; font-weight: bold; }',
            '        .passed { color: #27ae60; }',
            '        .failed { color: #e74c3c; }',
            '        .failure-card { background: #fff; border-left: 4px solid #e74c3c; padding: 20px; margin: 20px 0; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }',
            '        .test-name { font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }',
            '        .error-section { background: #fee; padding: 15px; border-radius: 4px; margin: 10px 0; font-family: monospace; font-size: 13px; }',
            '        .ai-section { background: #e8f5e9; padding: 15px; border-radius: 4px; margin: 10px 0; }',
            '        .ai-section h4 { margin-top: 0; color: #2e7d32; }',
            '        .ai-content { white-space: pre-wrap; line-height: 1.6; }',
            '        .timestamp { color: #95a5a6; font-size: 12px; }',
            '        .emoji { font-size: 20px; margin-right: 5px; }',
            '    </style>',
            '</head>',
            '<body>',
            '    <div class="container">',
            f'        <h1><span class="emoji">🤖</span>AI Failure Analysis Report</h1>',
            f'        <p class="timestamp">Generated: {analysis_data["generated_at"]}</p>',
            '',
            '        <div class="summary">',
            f'            <div class="summary-stat">',
            f'                <div class="label">Total Tests</div>',
            f'                <div class="value">{analysis_data["total_tests"]}</div>',
            f'            </div>',
            f'            <div class="summary-stat">',
            f'                <div class="label">Passed</div>',
            f'                <div class="value passed">{analysis_data["passed_tests"]}</div>',
            f'            </div>',
            f'            <div class="summary-stat">',
            f'                <div class="label">Failed</div>',
            f'                <div class="value failed">{analysis_data["failed_tests"]}</div>',
            f'            </div>',
            '        </div>',
        ]
        
        if analysis_data['analyses']:
            html_parts.append('        <h2>Failure Analysis</h2>')
            for idx, analysis in enumerate(analysis_data['analyses'], 1):
                html_parts.extend([
                    f'        <div class="failure-card">',
                    f'            <div class="test-name">#{idx}: {analysis["test_name"]}</div>',
                    f'            <div class="error-section">',
                    f'                <strong>Error Message:</strong><br>',
                    f'                {analysis["error_message"]}',
                    f'            </div>',
                    f'            <div class="ai-section">',
                    f'                <h4><span class="emoji">💡</span>AI Analysis & Recommendations</h4>',
                    f'                <div class="ai-content">{analysis["ai_analysis"]}</div>',
                    f'            </div>',
                    f'        </div>',
                ])
        else:
            html_parts.append('        <p>No failures to analyze. All tests passed! 🎉</p>')
        
        html_parts.extend([
            '    </div>',
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_parts)


class FailureCollector(ResultVisitor):
    """Visitor to collect failed test information from Robot Framework results."""
    
    def __init__(self, failures_list):
        self.failures = failures_list
    
    def visit_test(self, test):
        """Visit each test and collect failure information."""
        if test.status == 'FAIL':
            failure_info = {
                'test_name': test.name,
                'error_message': test.message,
                'steps': self._extract_steps(test)
            }
            self.failures.append(failure_info)
    
    def _extract_steps(self, test):
        """Extract test steps for context."""
        steps = []
        for kw in test.body:
            if hasattr(kw, 'name') and kw.name:
                steps.append(f"  {kw.name}")
        return steps[:10]  # Limit to first 10 steps for context


# Standalone script mode
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ai_failure_analyzer.py <path_to_output.xml>")
        sys.exit(1)
    
    output_xml = sys.argv[1]
    
    if not os.path.exists(output_xml):
        print(f"Error: File not found: {output_xml}")
        sys.exit(1)
    
    analyzer = AIFailureAnalyzer()
    report_path = analyzer.generate_analysis_report(output_xml)
    print(f"\n✅ Done! Open the report in your browser: {report_path}")
