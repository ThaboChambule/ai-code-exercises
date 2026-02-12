from datetime import datetime


# ============================================================================
# INPUT VALIDATION FUNCTIONS
# ============================================================================

def validate_report_parameters(sales_data, report_type, output_format, date_range):
    """
    Validate all input parameters for the sales report.
    
    Parameters:
    - sales_data: List of sales transactions
    - report_type: Type of report to generate
    - output_format: Format for output
    - date_range: Optional date range filter
    
    Raises:
    - ValueError: If any parameter is invalid
    """
    if not sales_data or not isinstance(sales_data, list):
        raise ValueError("Sales data must be a non-empty list")

    if report_type not in ['summary', 'detailed', 'forecast']:
        raise ValueError("Report type must be 'summary', 'detailed', or 'forecast'")

    if output_format not in ['pdf', 'excel', 'html', 'json']:
        raise ValueError("Output format must be 'pdf', 'excel', 'html', or 'json'")

    if date_range:
        if 'start' not in date_range or 'end' not in date_range:
            raise ValueError("Date range must include 'start' and 'end' dates")


# ============================================================================
# DATA FILTERING FUNCTIONS
# ============================================================================

def filter_by_date_range(sales_data, date_range):
    """
    Filter sales data by a specified date range.
    
    Parameters:
    - sales_data: List of sales transactions
    - date_range: Dict with 'start' and 'end' dates
    
    Returns:
    - Filtered list of sales transactions
    
    Raises:
    - ValueError: If start date is after end date
    """
    if not date_range:
        return sales_data

    start_date = datetime.strptime(date_range['start'], '%Y-%m-%d')
    end_date = datetime.strptime(date_range['end'], '%Y-%m-%d')

    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")

    filtered_data = []
    for sale in sales_data:
        sale_date = datetime.strptime(sale['date'], '%Y-%m-%d')
        if start_date <= sale_date <= end_date:
            filtered_data.append(sale)

    return filtered_data


def apply_additional_filters(sales_data, filters):
    """
    Apply additional filters to sales data.
    
    Parameters:
    - sales_data: List of sales transactions
    - filters: Dict of filters to apply (key-value pairs)
    
    Returns:
    - Filtered list of sales transactions
    """
    if not filters:
        return sales_data

    filtered_data = sales_data
    for key, value in filters.items():
        if isinstance(value, list):
            filtered_data = [sale for sale in filtered_data if sale.get(key) in value]
        else:
            filtered_data = [sale for sale in filtered_data if sale.get(key) == value]

    return filtered_data


def handle_empty_data(output_format):
    """
    Handle the case when no data matches the filter criteria.
    
    Parameters:
    - output_format: Desired output format
    
    Returns:
    - Empty report structure based on format
    """
    print("Warning: No data matches the specified criteria")
    
    if output_format == 'json':
        return {"message": "No data matches the specified criteria", "data": []}
    else:
        return _generate_empty_report(None, output_format)


# ============================================================================
# METRICS CALCULATION FUNCTIONS
# ============================================================================

def calculate_basic_metrics(sales_data):
    """
    Calculate basic sales metrics.
    
    Parameters:
    - sales_data: List of sales transactions
    
    Returns:
    - Dict containing total_sales, avg_sale, max_sale, min_sale
    """
    total_sales = sum(sale['amount'] for sale in sales_data)
    avg_sale = total_sales / len(sales_data)
    max_sale = max(sales_data, key=lambda x: x['amount'])
    min_sale = min(sales_data, key=lambda x: x['amount'])

    return {
        'total_sales': total_sales,
        'avg_sale': avg_sale,
        'max_sale': max_sale,
        'min_sale': min_sale
    }


def group_sales_data(sales_data, grouping):
    """
    Group sales data by a specified field.
    
    Parameters:
    - sales_data: List of sales transactions
    - grouping: Field to group by (e.g., 'product', 'category', 'region')
    
    Returns:
    - Dict of grouped data with counts, totals, and averages
    """
    if not grouping:
        return None

    grouped_data = {}
    for sale in sales_data:
        key = sale.get(grouping, 'Unknown')
        if key not in grouped_data:
            grouped_data[key] = {
                'count': 0,
                'total': 0,
                'items': []
            }

        grouped_data[key]['count'] += 1
        grouped_data[key]['total'] += sale['amount']
        grouped_data[key]['items'].append(sale)

    # Calculate averages for each group
    for key in grouped_data:
        grouped_data[key]['average'] = grouped_data[key]['total'] / grouped_data[key]['count']

    return grouped_data


# ============================================================================
# REPORT GENERATION FUNCTIONS
# ============================================================================

def build_base_report(report_type, date_range, filters, metrics):
    """
    Build the base report structure with common data.
    
    Parameters:
    - report_type: Type of report
    - date_range: Date range used for filtering
    - filters: Filters applied to data
    - metrics: Dict of calculated metrics
    
    Returns:
    - Base report dict with summary information
    """
    return {
        'report_type': report_type,
        'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': date_range,
        'filters': filters,
        'summary': {
            'total_sales': metrics['total_sales'],
            'transaction_count': metrics['transaction_count'],
            'average_sale': metrics['avg_sale'],
            'max_sale': {
                'amount': metrics['max_sale']['amount'],
                'date': metrics['max_sale']['date'],
                'details': metrics['max_sale']
            },
            'min_sale': {
                'amount': metrics['min_sale']['amount'],
                'date': metrics['min_sale']['date'],
                'details': metrics['min_sale']
            }
        }
    }


def add_grouping_to_report(report_data, grouped_data, grouping, total_sales):
    """
    Add grouping data to the report.
    
    Parameters:
    - report_data: Base report dict to update
    - grouped_data: Grouped sales data
    - grouping: Field used for grouping
    - total_sales: Total sales amount for percentage calculation
    """
    if not grouped_data:
        return

    report_data['grouping'] = {
        'by': grouping,
        'groups': {}
    }

    for key, data in grouped_data.items():
        report_data['grouping']['groups'][key] = {
            'count': data['count'],
            'total': data['total'],
            'average': data['average'],
            'percentage': (data['total'] / total_sales) * 100
        }


def add_detailed_transactions(report_data, sales_data):
    """
    Add detailed transaction information to the report.
    
    Parameters:
    - report_data: Base report dict to update
    - sales_data: List of sales transactions
    """
    report_data['transactions'] = []

    for sale in sales_data:
        transaction = {k: v for k, v in sale.items()}

        # Add calculated fields
        if 'tax' in sale and 'amount' in sale:
            transaction['pre_tax'] = sale['amount'] - sale['tax']

        if 'cost' in sale and 'amount' in sale:
            transaction['profit'] = sale['amount'] - sale['cost']
            transaction['margin'] = (transaction['profit'] / sale['amount']) * 100

        report_data['transactions'].append(transaction)


def calculate_forecast_data(sales_data):
    """
    Calculate forecast data including trends and projections.
    
    Parameters:
    - sales_data: List of sales transactions
    
    Returns:
    - Dict containing monthly sales, growth rates, and projections
    """
    # Group sales by month
    monthly_sales = {}
    for sale in sales_data:
        sale_date = datetime.strptime(sale['date'], '%Y-%m-%d')
        month_key = f"{sale_date.year}-{sale_date.month:02d}"

        if month_key not in monthly_sales:
            monthly_sales[month_key] = 0

        monthly_sales[month_key] += sale['amount']

    # Sort months and calculate growth rates
    sorted_months = sorted(monthly_sales.keys())
    growth_rates = []

    for i in range(1, len(sorted_months)):
        prev_month = sorted_months[i-1]
        curr_month = sorted_months[i]

        prev_amount = monthly_sales[prev_month]
        curr_amount = monthly_sales[curr_month]

        if prev_amount > 0:
            growth_rate = ((curr_amount - prev_amount) / prev_amount) * 100
            growth_rates.append(growth_rate)

    # Calculate average growth rate
    avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0

    # Generate forecast for next 3 months
    forecast = {}

    if sorted_months:
        last_month = sorted_months[-1]
        last_amount = monthly_sales[last_month]

        year, month = map(int, last_month.split('-'))

        for i in range(1, 4):
            month += 1
            if month > 12:
                month = 1
                year += 1

            forecast_month = f"{year}-{month:02d}"
            forecast_amount = last_amount * (1 + (avg_growth_rate / 100))

            forecast[forecast_month] = forecast_amount
            last_amount = forecast_amount

    return {
        'monthly_sales': monthly_sales,
        'growth_rates': {sorted_months[i]: growth_rates[i-1] for i in range(1, len(sorted_months))},
        'average_growth_rate': avg_growth_rate,
        'projected_sales': forecast
    }


def add_forecast_to_report(report_data, sales_data):
    """
    Add forecast data to the report.
    
    Parameters:
    - report_data: Base report dict to update
    - sales_data: List of sales transactions
    """
    forecast_data = calculate_forecast_data(sales_data)
    report_data['forecast'] = forecast_data


def generate_charts_data(sales_data, grouped_data, grouping):
    """
    Generate chart data for visualizations.
    
    Parameters:
    - sales_data: List of sales transactions
    - grouped_data: Grouped sales data (optional)
    - grouping: Field used for grouping (optional)
    
    Returns:
    - Dict containing chart data structures
    """
    charts_data = {}

    # Sales over time chart
    time_chart = {'labels': [], 'data': []}
    date_sales = {}

    for sale in sales_data:
        if sale['date'] not in date_sales:
            date_sales[sale['date']] = 0
        date_sales[sale['date']] += sale['amount']

    for date in sorted(date_sales.keys()):
        time_chart['labels'].append(date)
        time_chart['data'].append(date_sales[date])

    charts_data['sales_over_time'] = time_chart

    # Add pie chart for grouping if applicable
    if grouping and grouped_data:
        pie_chart = {'labels': [], 'data': []}

        for key, data in grouped_data.items():
            pie_chart['labels'].append(key)
            pie_chart['data'].append(data['total'])

        charts_data['sales_by_' + grouping] = pie_chart

    return charts_data


def add_charts_to_report(report_data, sales_data, grouped_data, grouping):
    """
    Add chart data to the report.
    
    Parameters:
    - report_data: Base report dict to update
    - sales_data: List of sales transactions
    - grouped_data: Grouped sales data (optional)
    - grouping: Field used for grouping (optional)
    """
    charts_data = generate_charts_data(sales_data, grouped_data, grouping)
    report_data['charts'] = charts_data


# ============================================================================
# OUTPUT FORMATTING FUNCTIONS
# ============================================================================

def format_output(report_data, output_format, include_charts):
    """
    Format the report data according to the requested output format.
    
    Parameters:
    - report_data: Complete report data dict
    - output_format: Desired output format
    - include_charts: Whether charts are included
    
    Returns:
    - Formatted report (dict for JSON, file path for others)
    """
    if output_format == 'json':
        return report_data
    elif output_format == 'html':
        return _generate_html_report(report_data, include_charts)
    elif output_format == 'excel':
        return _generate_excel_report(report_data, include_charts)
    elif output_format == 'pdf':
        return _generate_pdf_report(report_data, include_charts)


# ============================================================================
# MAIN REFACTORED FUNCTION
# ============================================================================

def generate_sales_report(sales_data, report_type='summary', date_range=None,
                         filters=None, grouping=None, include_charts=False,
                         output_format='pdf'):
    """
    Generate a comprehensive sales report based on provided data and parameters.

    This refactored version uses helper functions to separate concerns and
    improve maintainability. Each responsibility is isolated into its own function.

    Parameters:
    - sales_data: List of sales transactions
    - report_type: 'summary', 'detailed', or 'forecast'
    - date_range: Dict with 'start' and 'end' dates
    - filters: Dict of filters to apply
    - grouping: How to group data ('product', 'category', 'customer', 'region')
    - include_charts: Whether to include charts/visualizations
    - output_format: 'pdf', 'excel', 'html', or 'json'

    Returns:
    - Report data or file path depending on output_format
    """
    # 1. Validate all input parameters
    validate_report_parameters(sales_data, report_type, output_format, date_range)

    # 2. Apply date range filter
    sales_data = filter_by_date_range(sales_data, date_range)

    # 3. Apply additional filters
    sales_data = apply_additional_filters(sales_data, filters)

    # 4. Handle empty data case
    if not sales_data:
        return handle_empty_data(output_format)

    # 5. Calculate basic metrics
    metrics = calculate_basic_metrics(sales_data)
    metrics['transaction_count'] = len(sales_data)

    # 6. Group data if specified
    grouped_data = group_sales_data(sales_data, grouping)

    # 7. Build base report structure
    report_data = build_base_report(report_type, date_range, filters, metrics)

    # 8. Add grouping data if applicable
    add_grouping_to_report(report_data, grouped_data, grouping, metrics['total_sales'])

    # 9. Add report-type-specific data
    if report_type == 'detailed':
        add_detailed_transactions(report_data, sales_data)
    elif report_type == 'forecast':
        add_forecast_to_report(report_data, sales_data)

    # 10. Add charts if requested
    if include_charts:
        add_charts_to_report(report_data, sales_data, grouped_data, grouping)

    # 11. Format and return output
    return format_output(report_data, output_format, include_charts)


# ============================================================================
# HELPER FUNCTIONS (Placeholder implementations)
# ============================================================================

def _generate_empty_report(report_type, output_format):
    """Generate an empty report file."""
    pass


def _generate_html_report(report_data, include_charts):
    """Generate HTML report."""
    pass


def _generate_excel_report(report_data, include_charts):
    """Generate Excel report."""
    pass


def _generate_pdf_report(report_data, include_charts):
    """Generate PDF report."""
    pass
