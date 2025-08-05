-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 05, 2025 at 03:47 PM
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
-- Database: `LOCK`
--

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `message`, `created_at`) VALUES
(279, 'PIN access denied   --------   2024-12-31 20:23:50', '2025-01-02 16:39:22'),
(280, 'PIN access denied   --------   2024-12-31 20:23:50', '2025-01-02 16:39:29'),
(281, 'PIN access denied   --------   2024-12-31 20:23:50', '2025-01-02 16:39:34'),
(282, 'PIN access denied   --------   2024-12-31 20:23:50', '2025-01-02 16:39:40'),
(283, 'PIN access denied   --------   2024-12-31 20:23:50', '2025-01-02 16:39:45'),
(284, 'PIN access granted   --------   2024-12-31 20:40:02', '2025-01-02 16:42:39'),
(285, 'Fingerprint access granted   --------   2024-12-31 20:47:57', '2025-01-02 16:50:30'),
(286, 'PIN access granted   --------   2024-12-31 20:56:19', '2025-01-02 16:58:55'),
(287, 'Fingerprint access denied   --------   2024-12-31 20:56:47', '2025-01-02 16:59:22'),
(288, 'Fingerprint access denied   --------   2024-12-31 20:58:16', '2025-01-02 17:00:52'),
(289, 'PIN access granted   --------   2024-12-31 21:04:26', '2025-01-02 17:07:02'),
(290, 'Three failed attempts detected!', '2025-01-02 17:10:51'),
(291, 'Fingerprint access denied   --------   2024-12-31 21:08:18', '2025-01-02 17:11:02'),
(292, 'Three failed attempts detected!', '2025-01-02 17:11:28'),
(293, 'PIN access denied   --------   2024-12-31 21:08:54', '2025-01-02 17:11:38'),
(294, 'System ready', '2025-01-03 04:36:44'),
(295, 'PIN access granted   --------   2024-12-31 21:45:25', '2025-01-03 04:37:22'),
(296, 'Fingerprint access granted   --------   2024-12-31 21:52:10', '2025-01-03 04:44:03'),
(297, 'Fingerprint access denied   --------   2024-12-31 21:52:51', '2025-01-03 04:44:44'),
(298, 'Fingerprint access denied   --------   2024-12-31 22:20:56', '2025-01-03 06:59:50'),
(299, 'Three failed attempts detected!', '2025-01-03 07:01:24'),
(300, 'Fingerprint access denied   --------   2024-12-31 22:26:32', '2025-01-03 07:01:35'),
(301, 'Three failed attempts detected!', '2025-01-03 08:40:36'),
(302, 'Fingerprint access denied   --------   2025-01-01 00:05:39', '2025-01-03 08:40:49'),
(303, 'Fingerprint enrollment failed   --------   2025-01-01 00:15:02', '2025-01-03 08:50:00'),
(304, 'Voice registration failed   --------   2025-01-01 00:16:47', '2025-01-03 08:51:44'),
(305, 'Three failed attempts detected!', '2025-01-03 08:56:02'),
(306, 'PIN access denied   --------   2025-01-01 00:21:07', '2025-01-03 08:56:13'),
(307, 'Three failed attempts detected!', '2025-01-03 08:56:54'),
(308, 'PIN access denied   --------   2025-01-01 00:22:00', '2025-01-03 08:57:07'),
(309, 'System ready', '2025-01-03 09:05:08'),
(310, 'Fingerprint access denied   --------   2025-01-01 00:54:18', '2025-01-03 09:29:12'),
(311, 'Fingerprint access denied   --------   2025-01-01 01:12:44', '2025-01-03 09:47:37'),
(312, 'Three failed attempts detected!', '2025-01-03 09:54:19'),
(313, 'Voice access denied   --------   2025-01-01 01:19:25', '2025-01-03 09:54:29'),
(314, 'Fingerprint access granted   --------   2025-01-01 01:30:19', '2025-01-03 10:05:17'),
(315, 'Fingerprint access denied   --------   2025-01-01 01:37:01', '2025-01-03 10:11:56'),
(316, 'Fingerprint access granted   --------   2025-01-01 01:37:22', '2025-01-03 10:12:24'),
(317, 'PIN access granted   --------   2025-01-01 01:37:53', '2025-01-03 10:12:47'),
(318, 'Voice access denied   --------   2025-01-01 01:42:50', '2025-01-03 10:17:46'),
(319, 'Three failed attempts detected!', '2025-01-03 10:25:16'),
(320, 'Voice access denied   --------   2025-01-01 01:50:21', '2025-01-03 10:25:31'),
(321, 'Three failed attempts detected!', '2025-01-03 10:37:59'),
(322, 'Fingerprint access denied   --------   2025-01-01 02:03:06', '2025-01-03 10:38:12'),
(323, 'Three failed attempts detected!', '2025-01-03 11:02:20'),
(324, 'Voice access denied   --------   2025-01-01 02:27:23', '2025-01-03 11:02:32'),
(325, 'Fingerprint access granted   --------   2025-01-01 02:32:35', '2025-01-03 11:07:32'),
(326, 'Fingerprint access granted   --------   2025-01-01 03:06:45', '2025-01-03 13:12:51'),
(327, 'Fingerprint access denied   --------   2025-01-01 03:19:35', '2025-01-03 13:20:39'),
(328, 'System ready', '2025-01-03 13:20:44'),
(329, 'Fingerprint access denied   --------   2025-01-01 03:31:45', '2025-01-03 13:32:49'),
(330, 'Fingerprint access denied   --------   2025-01-01 03:39:51', '2025-01-03 13:40:53'),
(331, 'Three failed attempts detected!', '2025-01-03 13:41:08'),
(332, 'Fingerprint access denied   --------   2025-01-01 03:40:07', '2025-01-03 13:41:18'),
(333, 'Three failed attempts detected!', '2025-01-03 13:52:45'),
(334, 'Fingerprint access denied   --------   2025-01-01 03:51:27', '2025-01-03 13:52:56'),
(335, 'Three failed attempts detected!', '2025-01-03 13:58:07'),
(336, 'Fingerprint access denied   --------   2025-01-01 03:57:04', '2025-01-03 13:58:18'),
(337, 'Three failed attempts detected!', '2025-01-03 14:00:23'),
(338, 'Fingerprint access denied   --------   2025-01-01 03:59:21', '2025-01-03 14:00:35'),
(339, 'Three failed attempts detected!', '2025-01-03 14:35:18'),
(340, 'Voice access denied   --------   2025-01-01 04:34:10', '2025-01-03 14:35:29'),
(341, 'Three failed attempts detected!', '2025-01-03 15:13:55'),
(342, 'Fingerprint access denied   --------   2025-01-01 05:12:48', '2025-01-03 15:14:08'),
(343, 'Fingerprint access granted   --------   2025-01-01 05:13:29', '2025-01-03 15:14:31'),
(344, 'Fingerprint access denied   --------   2025-01-01 05:14:00', '2025-01-03 15:15:03'),
(345, 'Three failed attempts detected!', '2025-01-03 15:15:22'),
(346, 'Fingerprint access denied   --------   2025-01-01 05:14:19', '2025-01-03 15:15:40'),
(347, 'System ready', '2025-01-03 15:57:55'),
(348, 'Fingerprint access denied   --------   2025-01-01 06:00:45', '2025-01-03 16:02:10'),
(349, 'Fingerprint enrollment failed   --------   2025-01-01 06:05:18', '2025-01-03 16:06:41'),
(350, 'Fingerprint access denied   --------   2025-01-01 06:05:35', '2025-01-03 16:06:56'),
(351, 'Three failed attempts detected!', '2025-01-03 16:07:12'),
(352, 'Fingerprint access denied   --------   2025-01-01 06:05:51', '2025-01-03 16:07:22'),
(353, 'PIN access granted   --------   2025-01-01 06:06:26', '2025-01-03 16:07:48'),
(354, 'Voice registered   --------   2025-01-01 06:07:06', '2025-01-03 16:08:29'),
(355, 'Three failed attempts detected!', '2025-01-03 16:09:14'),
(356, 'Voice access denied   --------   2025-01-01 06:07:50', '2025-01-03 16:09:27'),
(357, 'PIN access granted   --------   2025-01-01 07:19:15', '2025-01-03 17:20:38'),
(358, 'Three failed attempts detected!', '2025-01-03 17:21:09'),
(359, 'Fingerprint access denied   --------   2025-01-01 07:19:45', '2025-01-03 17:21:22'),
(360, 'Fingerprint access denied   --------   2025-01-01 07:29:01', '2025-01-03 22:53:50'),
(361, 'PIN access granted   --------   2025-01-01 07:30:08', '2025-01-03 22:54:25'),
(362, 'Fingerprint access denied   --------   2025-01-01 07:32:45', '2025-01-03 22:57:01'),
(363, 'Fingerprint access granted   --------   2025-01-01 08:20:17', '2025-01-03 23:44:31'),
(364, 'PIN access granted   --------   2025-01-01 08:22:54', '2025-01-03 23:47:08'),
(365, 'System ready', '2025-01-03 23:52:02'),
(366, 'Fingerprint access denied   --------   2025-01-01 08:42:35', '2025-01-04 00:06:48'),
(367, 'Fingerprint access denied   --------   2025-01-01 08:45:46', '2025-01-04 00:09:59'),
(368, 'Three failed attempts detected!', '2025-01-04 00:10:19'),
(369, 'Fingerprint access denied   --------   2025-01-01 08:46:04', '2025-01-04 00:10:29'),
(370, 'PIN access granted   --------   2025-01-01 08:48:21', '2025-01-04 00:12:34'),
(371, 'Voice registered   --------   2025-01-01 08:49:11', '2025-01-04 00:13:29'),
(372, 'Voice access granted   --------   2025-01-01 08:49:55', '2025-01-04 00:14:10'),
(373, 'Voice access granted   --------   2025-01-01 08:50:35', '2025-01-04 00:14:51'),
(374, 'Fingerprint access granted   --------   2025-01-01 08:51:00', '2025-01-04 00:15:15'),
(375, 'Fingerprint access granted   --------   2025-01-01 08:51:00', '2025-01-04 00:15:15'),
(376, 'Fingerprint enrolled successfully   --------   2025-01-01 09:00:33', '2025-01-04 00:24:48'),
(377, 'Voice access denied   --------   2025-01-01 09:11:46', '2025-01-04 00:35:59'),
(378, 'Voice access granted   --------   2025-01-01 09:19:43', '2025-01-04 00:43:55'),
(379, 'Voice access denied   --------   2025-01-01 09:20:37', '2025-01-04 00:44:52'),
(380, 'Voice access granted   --------   2025-01-01 09:20:55', '2025-01-04 00:45:09'),
(381, 'Voice access granted   --------   2025-01-01 09:20:55', '2025-01-04 00:45:09'),
(382, 'System ready', '2025-01-05 02:08:47'),
(383, 'Fingerprint access denied   --------   2025-01-01 10:36:26', '2025-01-05 02:10:51'),
(384, 'Voice access denied   --------   2025-01-01 13:35:14', '2025-01-05 05:09:37'),
(385, 'Three failed attempts detected!', '2025-01-05 05:40:53'),
(386, 'Fingerprint access denied   --------   2025-01-01 14:06:33', '2025-01-05 05:41:04'),
(387, 'Fingerprint access denied   --------   2025-01-01 16:01:38', '2025-01-05 11:36:17'),
(388, 'Fingerprint enrollment failed   --------   2025-01-01 16:05:06', '2025-01-05 11:38:24'),
(389, 'System ready', '2025-01-05 12:19:07'),
(390, 'Fingerprint access denied   --------   2025-01-05 20:52:47', '2025-01-05 12:52:45'),
(391, 'PIN access granted   --------   2025-01-05 21:17:55', '2025-01-05 13:17:55'),
(392, 'Fingerprint access denied   --------   2025-01-05 21:38:01', '2025-01-05 13:38:00'),
(393, 'Fingerprint access denied   --------   2025-01-11 08:39:01', '2025-01-11 02:04:09'),
(394, 'Fingerprint access denied   --------   2025-01-11 09:07:06', '2025-01-11 02:05:51'),
(395, 'Fingerprint access granted   --------   2025-01-11 09:07:33', '2025-01-11 02:06:17'),
(396, 'System ready', '2025-01-11 02:37:20'),
(397, 'Fingerprint enrolled successfully   --------   2025-01-11 09:25:36', '2025-01-11 02:38:35'),
(398, 'System ready', '2025-01-11 02:58:40'),
(399, 'Fingerprint access denied   --------   2025-01-11 09:46:13', '2025-01-11 02:59:33'),
(400, 'System ready', '2025-01-11 03:34:40'),
(401, 'Fingerprint access denied   --------   2025-01-11 10:22:03', '2025-01-11 03:35:22'),
(402, 'Fingerprint access granted   --------   2025-01-11 10:22:43', '2025-01-11 03:35:59'),
(403, 'Fingerprint access granted   --------   2025-01-11 10:23:09', '2025-01-11 03:36:26'),
(404, 'System ready', '2025-01-11 04:05:27'),
(405, 'Voice registration failed   --------   2025-01-11 10:54:40', '2025-01-11 04:08:01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=406;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
