# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Browser    │  │    Mobile    │  │   Desktop    │      │
│  │  (HTML/CSS)  │  │  (Responsive)│  │   (WebApp)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Flask Application (app.py)               │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │  Jinja2    │  │ Bootstrap  │  │   Static   │     │   │
│  │  │ Templates  │  │    CSS     │  │   Assets   │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Routes (Blueprints)                 │   │
│  │  ┌────────┐  ┌──────────┐  ┌─────────┐  ┌─────────┐│   │
│  │  │  Auth  │  │Dashboard │  │ Clients │  │Invoices ││   │
│  │  │ Routes │  │  Routes  │  │ Routes  │  │ Routes  ││   │
│  │  └────────┘  └──────────┘  └─────────┘  └─────────┘│   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Business Logic (Services)                │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │   │
│  │  │     PDF      │  │    Email     │  │  Invoice  │ │   │
│  │  │  Generator   │  │   Service    │  │Calculator │ │   │
│  │  └──────────────┘  └──────────────┘  └───────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              SQLAlchemy ORM (models/)                 │   │
│  │  ┌────────┐  ┌────────┐  ┌─────────┐  ┌──────────┐ │   │
│  │  │  User  │  │ Client │  │ Invoice │  │  Invoice │ │   │
│  │  │ Model  │  │ Model  │  │  Model  │  │   Item   │ │   │
│  │  └────────┘  └────────┘  └─────────┘  └──────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE LAYER                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         SQLite (Dev) / PostgreSQL (Prod)             │   │
│  │  ┌────────┐  ┌────────┐  ┌─────────┐  ┌──────────┐ │   │
│  │  │ users  │  │clients │  │invoices │  │ invoice_ │ │   │
│  │  │ table  │  │ table  │  │  table  │  │items tbl │ │   │
│  │  └────────┘  └────────┘  └─────────┘  └──────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     SMTP     │  │   ReportLab  │  │   Storage    │      │
│  │ Email Server │  │  PDF Engine  │  │  (S3/Local)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Client Layer
- **Browser**: Modern web browsers (Chrome, Firefox, Safari, Edge)
- **Responsive Design**: Bootstrap 5 for mobile-first design
- **Progressive Enhancement**: Works without JavaScript, enhanced with JS

### 2. Presentation Layer (Flask)
- **Framework**: Flask 3.0
- **Template Engine**: Jinja2
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Session Management**: Flask-Login
- **Form Handling**: Flask-WTF

### 3. Application Layer

#### Routes (Blueprints)
```python
/auth/*          → Authentication (login, register, logout)
/dashboard/*     → Dashboard and analytics
/clients/*       → Client CRUD operations
/invoices/*      → Invoice CRUD operations
```

#### Services
- **PDFGenerator**: Creates professional PDF invoices using ReportLab
- **EmailService**: Sends emails via SMTP (invoices, reminders, confirmations)
- **InvoiceCalculator**: Handles all financial calculations

### 4. Data Access Layer (SQLAlchemy ORM)

#### Models
```python
User          → Authentication and user management
Client        → Customer information
Invoice       → Invoice header information
InvoiceItem   → Individual line items
```

#### Relationships
```
User (1) ──→ (N) Client
User (1) ──→ (N) Invoice
Client (1) ──→ (N) Invoice
Invoice (1) ──→ (N) InvoiceItem
```

### 5. Database Layer

#### SQLite (Development)
- File-based database
- Zero configuration
- Perfect for development and small deployments

#### PostgreSQL (Production)
- Robust, scalable
- ACID compliant
- Better for concurrent users

---

## Data Flow

### Creating an Invoice

```
1. User fills form → /invoices/create (POST)
                     ↓
2. Route validates data → invoices.py
                     ↓
3. Generate invoice number → Invoice.generate_invoice_number()
                     ↓
4. Create Invoice object → models/invoice.py
                     ↓
5. Add InvoiceItems → models/invoice_item.py
                     ↓
6. Calculate totals → InvoiceCalculator.calculate_totals()
                     ↓
7. Save to database → db.session.commit()
                     ↓
8. Redirect to view → /invoices/<id>
```

### Generating PDF

```
1. User clicks "Download PDF" → /invoices/<id>/pdf
                     ↓
2. Fetch invoice data → Invoice.query.get(id)
                     ↓
3. Generate PDF → PDFGenerator.generate_invoice()
                     ↓
4. Create PDF file → ReportLab
                     ↓
5. Save to static/invoices/
                     ↓
6. Send file to user → send_file()
```

### Sending Email

```
1. User clicks "Send Email" → /invoices/<id>/email (POST)
                     ↓
2. Generate PDF → PDFGenerator.generate_invoice()
                     ↓
3. Create email → EmailService.send_invoice_email()
                     ↓
4. Attach PDF → Message.attach()
                     ↓
5. Send via SMTP → mail.send()
                     ↓
6. Confirm to user → flash message
```

---

## Security Architecture

### Authentication
```
Password → bcrypt hash → Store in DB
Login → Check hash → Create session → Set cookie
```

### Session Management
- **Flask-Login**: Manages user sessions
- **Secure Cookies**: HTTPOnly, SameSite=Lax
- **Session Timeout**: 7 days (configurable)

### Authorization
- All routes protected with `@login_required`
- User can only access their own data
- Queries filtered by `user_id`

### Input Validation
- Form validation with Flask-WTF
- Email validation
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (Jinja2 auto-escaping)

---

## Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Clients Table
CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    company VARCHAR(100),
    gstin VARCHAR(15),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Invoices Table
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    date DATE NOT NULL,
    due_date DATE NOT NULL,
    subtotal FLOAT DEFAULT 0.0,
    tax_rate FLOAT DEFAULT 0.0,
    tax_amount FLOAT DEFAULT 0.0,
    discount FLOAT DEFAULT 0.0,
    total_amount FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'Pending',
    notes TEXT,
    terms TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    paid_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Invoice Items Table
CREATE TABLE invoice_items (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    description VARCHAR(255) NOT NULL,
    quantity FLOAT DEFAULT 1.0,
    price FLOAT NOT NULL,
    total FLOAT NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_clients_user_id ON clients(user_id);
CREATE INDEX idx_invoices_user_id ON invoices(user_id);
CREATE INDEX idx_invoices_client_id ON invoices(client_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_number ON invoices(invoice_number);
CREATE INDEX idx_invoice_items_invoice_id ON invoice_items(invoice_id);
```

---

## API Endpoints

### Authentication
```
POST   /auth/register          Register new user
POST   /auth/login             User login
GET    /auth/logout            User logout
```

### Dashboard
```
GET    /dashboard              Dashboard home
GET    /dashboard/api/stats    Get statistics (JSON)
GET    /dashboard/api/monthly-revenue  Monthly revenue data (JSON)
```

### Clients
```
GET    /clients                List all clients
GET    /clients/create         Show create form
POST   /clients/create         Create new client
GET    /clients/<id>           View client details
GET    /clients/<id>/edit      Show edit form
POST   /clients/<id>/edit      Update client
POST   /clients/<id>/delete    Delete client
GET    /clients/api/list       Get clients list (JSON)
```

### Invoices
```
GET    /invoices               List all invoices
GET    /invoices/create        Show create form
POST   /invoices/create        Create new invoice
GET    /invoices/<id>          View invoice details
GET    /invoices/<id>/edit     Show edit form
POST   /invoices/<id>/edit     Update invoice
POST   /invoices/<id>/delete   Delete invoice
POST   /invoices/<id>/status   Update invoice status
GET    /invoices/<id>/pdf      Download PDF
POST   /invoices/<id>/email    Send invoice via email
POST   /invoices/<id>/reminder Send payment reminder
```

---

## Technology Stack

### Backend
- **Python 3.9+**: Programming language
- **Flask 3.0**: Web framework
- **SQLAlchemy 2.0**: ORM
- **Flask-Login**: Authentication
- **Flask-Mail**: Email sending
- **bcrypt**: Password hashing
- **ReportLab**: PDF generation

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling
- **Bootstrap 5**: UI framework
- **Bootstrap Icons**: Icon library
- **JavaScript**: Interactivity
- **jQuery**: DOM manipulation
- **Chart.js**: Data visualization

### Database
- **SQLite**: Development database
- **PostgreSQL**: Production database

### Deployment
- **Gunicorn**: WSGI server
- **Nginx**: Reverse proxy
- **Docker**: Containerization
- **Render/Railway**: Cloud hosting

---

## Performance Considerations

### Database Optimization
- Indexes on frequently queried columns
- Lazy loading for relationships
- Query optimization with SQLAlchemy

### Caching (Future Enhancement)
- Flask-Caching for dashboard statistics
- Redis for session storage
- CDN for static assets

### Scalability
- Stateless application design
- Horizontal scaling with load balancer
- Database connection pooling

---

## Security Best Practices

✅ **Implemented:**
- Password hashing with bcrypt
- CSRF protection with Flask-WTF
- SQL injection prevention (ORM)
- XSS prevention (Jinja2 auto-escaping)
- Secure session cookies
- User data isolation

🔜 **Future Enhancements:**
- Rate limiting
- Two-factor authentication
- API key authentication
- Audit logging
- File upload validation
- Content Security Policy headers

---

## Monitoring & Logging

### Application Logs
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Error Tracking (Future)
- Sentry for error monitoring
- Application performance monitoring
- User analytics

---

## Backup Strategy

### Database Backup
```bash
# SQLite
cp database/invoices.db database/backups/invoices_$(date +%Y%m%d).db

# PostgreSQL
pg_dump invoice_db > backup_$(date +%Y%m%d).sql
```

### File Backup
- PDF invoices in `static/invoices/`
- Uploaded files in `static/uploads/`
- Regular backups to cloud storage (S3, Google Cloud Storage)

---

## Development Workflow

```
1. Feature Branch → git checkout -b feature/new-feature
2. Development → Code + Test
3. Commit → git commit -m "Add new feature"
4. Push → git push origin feature/new-feature
5. Pull Request → Review + Merge
6. Deploy → Automatic deployment (CI/CD)
```

---

## Testing Strategy

### Unit Tests
- Model methods
- Service functions
- Utility functions

### Integration Tests
- Route endpoints
- Database operations
- Email sending

### End-to-End Tests
- User workflows
- Invoice creation flow
- Payment flow

---

This architecture is designed to be:
- **Scalable**: Can handle growing user base
- **Maintainable**: Clean separation of concerns
- **Secure**: Multiple layers of security
- **Testable**: Easy to write tests
- **Deployable**: Multiple deployment options
