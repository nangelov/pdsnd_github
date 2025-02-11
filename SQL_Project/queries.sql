/*Q1: Q1: What is the number of film categories per customer? */
SELECT 
DISTINCT(cust.first_name || ' ' || cust.last_name) AS full_name,
count(cat.name) as number_of_film_categories
FROM customer cust
JOIN rental r ON r.customer_id = cust.customer_id
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film_category fc ON fc.film_id = i.film_id
JOIN category cat ON cat.category_id = fc.category_id
GROUP BY full_name
ORDER BY number_of_film_categories ASC;

/*Q2: How do the rental order counts of the two stores
compare on a monthly basis across all years in our data*/
SELECT 
EXTRACT(month FROM r.rental_date) as Rental_Month, 
EXTRACT(year FROM r.rental_date) as Rental_Year,
i.store_id,
count(r.rental_id) as count_rentals 
FROM rental r
JOIN inventory i ON i.inventory_id = r.inventory_id
GROUP BY Rental_Year, Rental_Month, i.store_id
ORDER BY Rental_Year, Rental_Month;

/* Q3: What is total paid amount per month in 2007 and by how
many customers?*/
SELECT 
sum(total_paid_amount),
payment_month, 
customer_name
FROM (SELECT 
      DISTINCT(c.first_name || ' ' || c.last_name) AS customer_name,
      to_char(p.payment_date, 'YYYY-MM') as payment_month,
      SUM(p.amount) as total_paid_amount
      FROM payment p
      JOIN customer c ON p.customer_id = c.customer_id
      WHERE EXTRACT(year FROM payment_date) = 2007
      GROUP BY payment_month, customer_name
      ORDER by payment_month) as sub_q
GROUP BY payment_month, customer_name;

/* Q4: What is average rental per family friendly categories and
per quartiles? */
WITH family_movies AS (
  SELECT 
    f.title AS film_title,
    c.name AS category_name,
    AVG(EXTRACT(DAY FROM (r.return_date - r.rental_date))) AS avg_rental_duration
  FROM film f
  JOIN film_category fc ON fc.film_id = f.film_id
  JOIN category c ON c.category_id = fc.category_id
  JOIN inventory i ON i.film_id = f.film_id
  JOIN rental r ON r.inventory_id = i.inventory_id
  WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
  GROUP BY f.title, c.name
)
SELECT 
  family_movies.film_title as title,
  family_movies.category_name,
  ROUND(CAST(family_movies.avg_rental_duration as numeric),2) as rental_duration,
  NTILE(4) OVER (ORDER BY family_movies.avg_rental_duration) AS standard_quartile
FROM family_movies
ORDER BY family_movies.category_name ASC, family_movies.film_title ASC;