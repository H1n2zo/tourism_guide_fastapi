-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 11, 2025 at 08:49 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tourism_guide`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `icon`, `created_at`) VALUES
(1, 'Tourist Spot', 'fa-camera', '2025-11-04 23:48:18'),
(2, 'Restaurant', 'fa-utensils', '2025-11-04 23:48:18'),
(3, 'Hotel', 'fa-bed', '2025-11-04 23:48:18'),
(4, 'Transport Terminal', 'fa-bus', '2025-11-04 23:48:18'),
(5, 'Landmark', 'fa-landmark', '2025-11-04 23:48:18'),
(6, 'Nature', 'fa-tree', '2025-11-04 23:48:18'),
(7, 'Shopping', 'fa-shopping-bag', '2025-11-04 23:48:18'),
(8, 'Entertainment', 'fa-film', '2025-11-04 23:48:18'),
(10, 'Comfort Room', 'fa-toilet', '2025-11-05 02:30:14'),
(11, 'Favorites', 'fa-heart', '2025-11-05 02:41:51'),
(12, 'Church', 'fa-church', '2025-11-05 06:07:10');

-- --------------------------------------------------------

--
-- Table structure for table `destinations`
--

CREATE TABLE `destinations` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `address` text DEFAULT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `contact_number` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  `opening_hours` varchar(100) DEFAULT NULL,
  `entry_fee` varchar(100) DEFAULT NULL,
  `rating` decimal(2,1) DEFAULT 0.0,
  `image_path` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `destinations`
--

INSERT INTO `destinations` (`id`, `name`, `category_id`, `description`, `address`, `latitude`, `longitude`, `contact_number`, `email`, `website`, `opening_hours`, `entry_fee`, `rating`, `image_path`, `is_active`, `created_at`, `updated_at`) VALUES
(8, 'Lake Danao Natural Park', 1, 'A guitar-shaped lake located in the highlands of Ormoc City. Perfect for nature lovers, kayaking, and picnics. The serene environment offers cool climate and stunning mountain views.', 'Barangay Lake Danao, Ormoc City, Leyte', 11.15420000, 124.78310000, '+63-053-255-2345', '', '', '6:00 AM - 6:00 PM', 'PHP 20', 5.0, 'destinations/1d5b324d-db76-44df-8e5f-d4d8affa3bb8_1765204606.jpg', 1, '2025-11-05 05:50:01', '2025-12-08 14:36:46'),
(11, 'Alto Peak Cafe', 2, '𝙏𝙖𝙩𝙖𝙠 𝙊𝙧𝙢𝙤𝙘, 𝙩𝙖𝙩𝙖𝙠 𝙨𝙖𝙧𝙖𝙥!\r\n\r\n𝘈𝘳𝘵𝘪𝘴𝘢𝘯 𝘤𝘩𝘰𝘤𝘰𝘭𝘢𝘵𝘦𝘴 𝘪𝘯𝘴𝘱𝘪𝘳𝘦𝘥 𝘣𝘺 𝘵𝘩𝘦 𝘸𝘢𝘳𝘮𝘵𝘩 𝘰𝘧 𝘍𝘪𝘭𝘪𝘱𝘪𝘯𝘰 𝘩𝘰𝘴𝘱𝘪𝘵𝘢𝘭𝘪𝘵𝘺 𝘢𝘯𝘥 𝘤𝘶𝘭𝘵𝘶𝘳𝘦.', 'Valle St. Purok IV., Brgy Dona Feliza Mejia,, Ormoc City, Philippines', 11.02000684, 124.60012127, '+63917 173 7758', 'altopeakchocolates@gmail.com', '', ' 6AM-8PM', 'Free', 5.0, 'destinations/25bf63db-f38b-4853-88db-4f169edbc238_1765204115.jpg', 1, '2025-11-05 05:50:01', '2025-12-08 14:29:57'),
(12, 'Sambawan Island Beach', 1, 'Pristine white sand beach with turquoise waters. Known for its stunning sandbar, coral reefs, and camping facilities. Great for island hopping.', 'Sambawan Island, Ormoc City, Leyte', 11.02110000, 124.52340000, '+63-917-345-6789', '', '', '24 Hours', 'PHP 150', 5.0, 'destinations/609e384b-774a-4bff-a12f-722a2479fb20_1765388909.jpg', 1, '2025-11-05 05:50:01', '2025-12-10 17:48:36'),
(13, 'Mahagnao Volcano Natural Park', 5, 'Features twin crater lakes, hot springs, and diverse wildlife. A protected area with hiking trails through pristine forests and geothermal features.', 'Barangay Mahagnao, Ormoc City, Leyte', 11.14440000, 124.75560000, '', '', '', '7:00 AM - 5:00 PM', 'PHP 30', 5.0, 'destinations/0db83540-4621-42f5-9f91-2081824fe7fe_1765386705.jpg', 1, '2025-11-05 05:59:34', '2025-12-10 17:11:51'),
(37, 'Ormoc City Plaza', 1, '...', '...', 11.00590000, 124.60750000, '+63-053-561-5200', 'ormoccity@gmail.com', '', '24 Hours', 'Free', 5.0, 'destinations/690b35ea7e743_1762342378.jpg', 1, '2025-11-05 06:04:26', '2025-11-05 11:32:58'),
(39, 'Ormoc City Superdome', 1, '...', '...', 11.00890000, 124.60890000, '+63-053-561-6789', '', '', '8:00 AM - 10:00 PM', 'Varies', 5.0, 'destinations/690b36df53283_1762342623.jpg', 1, '2025-11-05 06:04:26', '2025-11-05 11:37:03'),
(40, 'Ormoc Veterans Park', 1, '...', '...', 11.00450000, 124.60670000, '+63-053-561-5200', '', '', '24 Hours', 'Free', 5.0, 'destinations/690b36af1cdbe_1762342575.jpg', 1, '2025-11-05 06:04:26', '2025-11-05 11:36:15'),
(42, 'Ormoc Public Market', 7, 'Bustling local market offering fresh produce, seafood, local delicacies, and handicrafts. Best place to experience local culture and food.', 'Bonifacio Street, Ormoc City, Leyte', 11.00780000, 124.60780000, '+63-053-561-8901', '', '', '5:00 AM - 6:00 PM', '', 5.0, 'destinations/690b358e4342f_1762342286.jpg', 1, '2025-11-05 06:08:34', '2025-11-05 11:31:26'),
(44, 'Don Felipe Hotel', 3, 'Premier hotel in Ormoc City offering comfortable rooms, restaurant, function halls, and excellent service. Convenient location near city center.', 'Bonifacio Street, Ormoc City, Leyte', 11.00710000, 124.60820000, '+63-053-561-9012', 'info@donfelipehotel.com', '', '', '', 5.0, 'destinations/690afeb1e236f_1762328241.webp', 1, '2025-11-05 06:08:54', '2025-11-05 08:51:03'),
(45, 'GV Hotel Ormoc', 3, 'Budget-friendly hotel with clean rooms, air conditioning, and basic amenities. Perfect for travelers looking for affordable accommodation.', 'Real Street, Ormoc City, Leyte', 11.00630000, 124.60730000, '+63-053-561-9123', 'gvormoc@gvhotels.com.ph', '', '', '', 5.0, 'destinations/690b00c3bb9e6_1762328771.jpg', 1, '2025-11-05 06:08:54', '2025-11-05 08:51:03'),
(46, 'Ormoc Villa Hotel', 3, 'Mid-range hotel with modern facilities, swimming pool, restaurant, and conference rooms. Family-friendly with spacious rooms.', 'Aviles Street, Ormoc City, Leyte', 11.00810000, 124.60910000, '+63-053-561-9234', 'reservations@ormocvillahotel.com', '', '', '', 5.0, 'destinations/690b35305c563_1762342192.jpg', 1, '2025-11-05 06:08:54', '2025-11-05 11:29:52'),
(47, 'Robinsons Place Ormoc', 7, 'Major shopping mall featuring department store, supermarket, cinema, restaurants, and retail shops. Air-conditioned and family-friendly.', 'Real Street, Ormoc City, Leyte', 11.02516804, 124.60520309, '+63-053-561-9345', '', '', '10:00 AM - 9:00 PM', '', 5.0, 'destinations/690b2c8c9acbc_1762339980.webp', 0, '2025-11-05 06:09:08', '2025-12-11 06:57:57'),
(49, 'Ormoc Pasalubong Center', 7, 'One-stop shop for local products and souvenirs. Features Ormoc delicacies, handicrafts, and regional specialties. Perfect for gifts.', 'Rizal Avenue, Ormoc City, Leyte', 11.00650000, 124.60770000, '+63-917-789-0123', '', '', '8:00 AM - 7:00 PM', '', 5.0, 'destinations/690b3135da062_1762341173.jpg', 1, '2025-11-05 06:09:08', '2025-12-09 06:38:35'),
(52, 'Cafebeng', 2, 'ormoc’s micro café for artisan baked goods & pastries, housemade treats, and quality coffee & drinks—made fresh daily ♡', 'Bonifacio Street, Ormoc City', 11.00766951, 124.60900207, '', '', '', '11am-8pm', '', 0.0, 'destinations/3fb7c676-252a-426a-b7a6-a40317a1fab4_1765380337.jpg', 1, '2025-12-10 15:25:37', '2025-12-10 15:25:37'),
(53, 'Lake Janagdan', 6, 'Lake Janagdan is in the eastern part of Ormocc City and surrounded by green and diverse vegetation. It is part of the Aminduen mountain ranges, and is a crater lake measuring about 200 meters in diameter. This crater lake is in the caldera of Mount Janagdan, an already dormant volcano. It is 1120 meters above sea level, and the hike would take about 2 hours. After the cathartic hike, you will be greeted by the cold waters of the lake. There are kayak boats and life jackets for use in the area. ', 'Brgy. Cabintan, Ormoc City, Leyte', 11.09905551, 124.71735517, '', '', '', '', '', 0.0, 'destinations/8c4efa69-3aab-47a2-8008-a2534b7d456e_1765381396.jpg', 1, '2025-12-10 15:43:16', '2025-12-10 15:43:16'),
(54, 'Ormoc City Museum', 1, 'The 1947 Old City Hall was replaced by the Ormoc City Museum, or People\'s Museum, to establish a location where art, culture, and history are cherished.', 'Aviles Street, Ormoc City, Leyte', 11.00503664, 124.60891872, '', '', '', '10am-4pm', '', 0.0, 'destinations/4ca5da1a-5fc1-4307-bdb6-e601a6d0f161_1765384304.jpg', 1, '2025-12-10 16:31:44', '2025-12-10 16:31:44'),
(55, 'Our Lady of Assumption\'s Shrine', 12, 'The Our Lady of Assumption statue is a towering 10.9728 meters tall statue, located in Barangay Mantahan.  Believed to be miraculous, “Mama Mary,” as it is popularly called, is said to be the protector of the City of Maasin.', 'Jalleca Hills, Brgy M.antahan, Maasin City, Southern Leyte', 10.13589958, 124.84624878, '', '', '', 'Open 24H', 'Free', 0.0, 'destinations/317068a0-fa1c-482a-a465-1fedcd33a591_1765384899.jpg', 1, '2025-12-10 16:41:39', '2025-12-10 16:41:39'),
(56, 'Ormoc City Transport Terminal', 4, 'The Ormoc City Transport Terminal Robinsons, also referred to as the Robinsons Place Ormoc Transport Terminal, is a major transportation hub in Ormoc City, Leyte, Philippines, located at the Robinsons Place Ormoc mall complex.', 'Brgy. Cogon, Ormoc City, Leyte', 11.02634380, 124.60555772, '', '', '', '', '', 0.0, 'destinations/4d692254-0283-45aa-b365-df102fca1423_1765385621.avif', 1, '2025-12-10 16:53:41', '2025-12-10 16:53:41'),
(57, 'Sayahan Falls', 6, 'A beautiful natural gem located in Ormoc City, Leyte, Philippines. It\'s known for its multi-tiered waterfalls and crystal-clear waters. The falls are surrounded by lush greenery and mossy rock formations, making it a picturesque spot for nature lovers and adventure seekers.', 'Brgy. Gaas, Ormoc City', 11.01211529, 124.72201146, '', '', '', '', '', 0.0, 'destinations/235b164b-fecb-43af-95fd-0db88550d7ca_1765386325.webp', 1, '2025-12-10 17:04:59', '2025-12-10 17:05:25'),
(58, 'Mother of the Reedeemer Parish', 12, 'The Mother of the Redeemer Parish in Ormoc is a community-oriented Catholic church that originated as a chapel in the Cogon district, an area historically known for its vast \"cogon\" grass vegetation.', 'Fatima Cogon, Ormoc City, Leyte', 11.01894847, 124.60385452, '+63 999 416 5258', '', '', '', '', 0.0, 'destinations/7b404c8c-3ac0-48c1-ad15-448de90ce042_1765388674.jpg', 1, '2025-12-10 17:44:34', '2025-12-10 17:44:34');

-- --------------------------------------------------------

--
-- Table structure for table `destination_images`
--

CREATE TABLE `destination_images` (
  `id` int(11) NOT NULL,
  `destination_id` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `caption` varchar(200) DEFAULT NULL,
  `is_primary` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `destination_images`
--

INSERT INTO `destination_images` (`id`, `destination_id`, `image_path`, `caption`, `is_primary`, `created_at`) VALUES
(4, 44, 'destinations/690afeb1ea56d_1762328241.webp', '', 0, '2025-11-05 07:37:21'),
(5, 44, 'destinations/690afec9924f0_1762328265.webp', '', 0, '2025-11-05 07:37:45'),
(6, 45, 'destinations/690b00c3c4ab0_1762328771.jpg', '', 0, '2025-11-05 07:46:11'),
(8, 47, 'destinations/690b2806622aa_1762338822.jpg', '', 0, '2025-11-05 10:33:42'),
(10, 37, 'destinations/690b35ea8607b_1762342378.jpg', '', 0, '2025-11-05 11:32:58'),
(11, 37, 'destinations/690b35ff3e7c8_1762342399.jpg', '', 0, '2025-11-05 11:33:19'),
(12, 37, 'destinations/690b3610e81f3_1762342416.jpg', '', 0, '2025-11-05 11:33:36'),
(13, 8, 'destinations/690b3722b701d_1762342690.jpg', '', 0, '2025-11-05 11:38:10'),
(15, 8, 'destinations/222043e0-c024-4cc6-856b-9fac14e6932f_1765204606.webp', '', 0, '2025-12-08 14:36:46');

-- --------------------------------------------------------

--
-- Stand-in structure for view `destination_ratings`
-- (See below for the actual view)
--
CREATE TABLE `destination_ratings` (
`id` int(11)
,`name` varchar(200)
,`review_count` bigint(21)
,`average_rating` decimal(12,1)
,`five_star` decimal(22,0)
,`four_star` decimal(22,0)
,`three_star` decimal(22,0)
,`two_star` decimal(22,0)
,`one_star` decimal(22,0)
);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `destination_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` >= 1 and `rating` <= 5),
  `comment` text DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `destination_id`, `user_id`, `user_name`, `rating`, `comment`, `is_approved`, `created_at`) VALUES
(11, 8, NULL, 'Maria Santos', 3, 'Lake Danao is absolutely breathtaking! Perfect for a peaceful getaway. The guitar shape is amazing from the viewpoint.', 1, '2024-10-15 02:30:00'),
(12, 11, NULL, 'HinzoHana', 2, 'Wews', 1, '2025-11-05 08:43:11'),
(14, 11, NULL, 'Hello', 5, 'sample 2 ratings', 0, '2025-11-05 08:58:44'),
(21, 49, NULL, 'Jeramae', 5, 'I had a lot of options to choose from this place, absolutely a wonderful place to visit!', 1, '2025-12-06 03:25:47'),
(22, 49, NULL, 'Jojo', 5, 'so much foods but i don\'t have money, maybe next time', 1, '2025-12-06 03:27:30');

-- --------------------------------------------------------

--
-- Table structure for table `review_images`
--

CREATE TABLE `review_images` (
  `id` int(11) NOT NULL,
  `review_id` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review_images`
--

INSERT INTO `review_images` (`id`, `review_id`, `image_path`, `created_at`) VALUES
(1, 21, 'reviews/c7b1a80a-2799-4c88-bd10-3d1db7f8a270_1764991547.webp', '2025-12-06 11:25:47');

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

CREATE TABLE `routes` (
  `id` int(11) NOT NULL,
  `route_name` varchar(200) DEFAULT NULL,
  `origin_id` int(11) DEFAULT NULL,
  `destination_id` int(11) DEFAULT NULL,
  `transport_mode` enum('jeepney','taxi','bus','van','tricycle','walking') NOT NULL,
  `distance_km` decimal(6,2) DEFAULT NULL,
  `estimated_time_minutes` int(11) DEFAULT NULL,
  `base_fare` decimal(8,2) DEFAULT NULL,
  `fare_per_km` decimal(8,2) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `routes`
--

INSERT INTO `routes` (`id`, `route_name`, `origin_id`, `destination_id`, `transport_mode`, `distance_km`, `estimated_time_minutes`, `base_fare`, `fare_per_km`, `description`, `is_active`, `created_at`) VALUES
(36, 'Ormoc City Superdome to Robinsons Place Ormoc', 39, 47, 'taxi', 0.00, 10, 20.00, 1.00, 'Tricycles to The Wan Shop', 1, '2025-11-09 10:35:06');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` enum('ADMIN','USER') DEFAULT 'USER',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `role`, `created_at`) VALUES
(1, 'Admin', '$2y$10$1Rx1ytdO.DDgmbcZ3n0MBet/I3haMLn8IAc6NwUj/szZPuIjW7of.', 'admin@tourism.com', 'ADMIN', '2025-11-10 02:03:29'),
(2, 'Hans', '$2y$10$/ADtH0gaUpSr8ox4ihu2vOcwwsZWwLg8I5vNh6JJmlJSGzgTpd7x6', 'hansmichael.2005.gabor@gmail.com', 'USER', '2025-11-05 00:31:38'),
(7, 'Jessha', '$2y$10$UHxAWjNSmRQZDICCSLOE6.HNvR3SDQ9ciHtVfo1PqDAflYHUWgk16', 'jessha@gmail.com', 'USER', '2025-11-22 12:21:44'),
(12, 'jeraTG', '$2b$12$n5nQUaKhW67QuKHKHS957OJf6yJec9GS4xYm3MawURLKQwhY0USyC', 'jera@gmail.com', 'ADMIN', '2025-12-03 06:57:44'),
(13, 'jeraT', '$2b$12$0oaMVdReypbV4v8pQQvud.E8GRN4owOpoKq1Ruk7MemguvazMhv2.', 'ff@gmail.com', 'USER', '2025-12-03 07:11:35');

-- --------------------------------------------------------

--
-- Table structure for table `website_feedback`
--

CREATE TABLE `website_feedback` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` >= 1 and `rating` <= 5),
  `category` enum('usability','features','content','design','general') DEFAULT 'general',
  `feedback` text NOT NULL,
  `is_public` tinyint(1) DEFAULT 1,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `website_feedback`
--

INSERT INTO `website_feedback` (`id`, `user_id`, `user_name`, `email`, `rating`, `category`, `feedback`, `is_public`, `is_read`, `created_at`) VALUES
(4, 1, 'Admin', 'admin@tourism.com', 5, 'general', 'Im very satisfied', 1, 0, '2025-11-10 04:48:43'),
(7, NULL, 'Admin', 'hansmichael.gabor@evsu.edu.ph', 1, 'general', 'Error in recent feedback from visitors and map not showing directions', 1, 1, '2025-11-12 00:07:05');

-- --------------------------------------------------------

--
-- Structure for view `destination_ratings`
--
DROP TABLE IF EXISTS `destination_ratings`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `destination_ratings`  AS SELECT `d`.`id` AS `id`, `d`.`name` AS `name`, count(`r`.`id`) AS `review_count`, round(avg(`r`.`rating`),1) AS `average_rating`, sum(case when `r`.`rating` = 5 then 1 else 0 end) AS `five_star`, sum(case when `r`.`rating` = 4 then 1 else 0 end) AS `four_star`, sum(case when `r`.`rating` = 3 then 1 else 0 end) AS `three_star`, sum(case when `r`.`rating` = 2 then 1 else 0 end) AS `two_star`, sum(case when `r`.`rating` = 1 then 1 else 0 end) AS `one_star` FROM (`destinations` `d` left join `reviews` `r` on(`d`.`id` = `r`.`destination_id` and `r`.`is_approved` = 1)) GROUP BY `d`.`id`, `d`.`name` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `destinations`
--
ALTER TABLE `destinations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `destination_images`
--
ALTER TABLE `destination_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `destination_id` (`destination_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_reviews_destination` (`destination_id`),
  ADD KEY `idx_reviews_rating` (`rating`);

--
-- Indexes for table `review_images`
--
ALTER TABLE `review_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `review_id` (`review_id`),
  ADD KEY `ix_review_images_id` (`id`);

--
-- Indexes for table `routes`
--
ALTER TABLE `routes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `origin_id` (`origin_id`),
  ADD KEY `destination_id` (`destination_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `website_feedback`
--
ALTER TABLE `website_feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_feedback_rating` (`rating`),
  ADD KEY `idx_feedback_created` (`created_at`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `destinations`
--
ALTER TABLE `destinations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT for table `destination_images`
--
ALTER TABLE `destination_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `review_images`
--
ALTER TABLE `review_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `routes`
--
ALTER TABLE `routes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `website_feedback`
--
ALTER TABLE `website_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `destinations`
--
ALTER TABLE `destinations`
  ADD CONSTRAINT `destinations_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `destination_images`
--
ALTER TABLE `destination_images`
  ADD CONSTRAINT `destination_images_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `review_images`
--
ALTER TABLE `review_images`
  ADD CONSTRAINT `review_images_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `reviews` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `routes`
--
ALTER TABLE `routes`
  ADD CONSTRAINT `routes_ibfk_1` FOREIGN KEY (`origin_id`) REFERENCES `destinations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `routes_ibfk_2` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `website_feedback`
--
ALTER TABLE `website_feedback`
  ADD CONSTRAINT `website_feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
