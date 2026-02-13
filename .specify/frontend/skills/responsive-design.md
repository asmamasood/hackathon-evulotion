# Responsive Design Skill

## Purpose
Implement responsive UI designs that work across all device sizes and screen resolutions.

## Implementation Guidelines
- Use CSS Grid and Flexbox for responsive layouts
- Implement mobile-first approach
- Define proper breakpoints for different screen sizes
- Use relative units (rem, em, %) instead of fixed pixels
- Implement touch-friendly interactions

## Best Practices
- Follow accessibility standards (WCAG)
- Use semantic HTML elements
- Implement proper focus management
- Optimize for performance on mobile devices
- Test across different browsers and devices

## Example Usage
```
/* Using Tailwind CSS */
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card />
  <Card />
  <Card />
</div>

/* Custom CSS with media queries */
.container {
  width: 100%;
  padding: 0 1rem;
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
    margin: 0 auto;
  }
}
```