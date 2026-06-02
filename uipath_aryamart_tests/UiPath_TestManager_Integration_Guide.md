# UiPath Test Manager Integration & Execution Guide
### Project Name: AryaMartUiPathTests | Version: 1.0.0
### Platform: UiPath Test Suite & Studio (Windows target)

This guide walks you through connecting your local **AryaMart UiPath Test Automation Project** to **UiPath Test Manager** and orchestrating end-to-end execution.

---

## 🏗️ 1. Opening the Project in UiPath Studio
1. Open **UiPath Studio** (ensure you are using version `2021.10` or higher to support modern testing projects).
2. Choose **Open Local Project** and navigate to your project directory:
   📁 [uipath_aryamart_tests](file:///d:/Projects/Scripts/uipath_aryamart_tests/)
3. Select and open [project.json](file:///d:/Projects/Scripts/uipath_aryamart_tests/project.json).
4. UiPath Studio will automatically restore the project dependencies (`UiPath.Testing.Activities` and `UiPath.UIAutomation.Activities`).

---

## 🔗 2. Connecting Studio to UiPath Test Manager
Before linking test cases, establish the connection between your Studio client and the Test Manager server instance:

1. In UiPath Studio, look at the bottom-right corner or go to the ribbon menu **Test Suite** tab.
2. Select **Test Manager Settings**.
3. In the dialog box:
   * **Test Manager URL**: Enter your Test Manager server URL (e.g., `https://testmanager.uipath.com/` or your custom enterprise tenant URL).
   * **Project**: Select your target Test Manager project (e.g., `AryaMart_Test_Suite`). If none exists, create one first in your Test Manager web portal.
4. Click **Connect**. A green connection indicator will confirm successful pairing.

---

## 🎯 3. Linking Studio Test Cases to Test Manager
Linking creates direct traceability between your physical workflow test automation files and the logical test specifications in Test Manager.

### Option A: Link from UiPath Studio (Recommended)
1. Go to the **Project panel** in Studio.
2. Right-click [TestCase_Login.xaml](file:///d:/Projects/Scripts/uipath_aryamart_tests/TestCase_Login.xaml).
3. Select **Link to Test Manager** from the context menu.
4. In the configuration popup:
   * **Requirement**: (Optional) Search and select a Requirement from your backlog (e.g., *REQ-101: User Login Auth*).
   * **Test Case**: Choose **Create New** (it will auto-populate with the test case name) or select an existing test case in Test Manager.
5. Click **OK**.
6. Repeat the process for [TestCase_AddToCart.xaml](file:///d:/Projects/Scripts/uipath_aryamart_tests/TestCase_AddToCart.xaml).

> [!NOTE]
> Once linked, Studio updates the project metadata. The test cases are now permanently mapped using the unique GUIDs `e0a1f0a1-7788-44d4-a131-7b7cfa374822` and `f5b2f5b2-8899-44d4-b242-8b8dfb485933`.

### Option B: Link from Test Manager Web UI
1. Open the **Test Manager Web Portal**.
2. Go to your **Test Cases** page and select a test case.
3. Click the **Automation** tab.
4. Under **Automation Details**, paste the unique testCaseId or select the workspace file path mapping to link them.

---

## 📦 4. Publishing to Orchestrator
To execute tests remotely via Test Manager, the package must be uploaded to UiPath Orchestrator:

1. Click **Publish** in the top ribbon of UiPath Studio.
2. In the publish wizard:
   * Set **Publish Options** ➔ **Destination** to `Orchestrator Tenant Process Feed`.
   * Under **Package Name**, use `AryaMartUiPathTests`.
3. Click **Publish**. A notification will appear once the package uploads successfully.

---

## 🚀 5. Executing Test Cases & Reviewing Results
You can trigger execution directly from Test Manager, which routes the request via Orchestrator to your local or virtual robot:

### Step 1: Create a Test Set in Test Manager
1. In the Test Manager web portal, go to **Test Sets**.
2. Click **Create Test Set** and name it `AryaMart Regression Cycle`.
3. Go to the **Test Cases** tab of the set, click **Add Test Cases**, and check `TestCase_Login` and `TestCase_AddToCart`.

### Step 2: Link Test Set to Orchestrator
1. Inside the Test Set page, go to the **Select Automation** section.
2. Select the Orchestrator **Environment/Folder** and the **Process** (`AryaMartUiPathTests`) you published in Step 4.

### Step 3: Trigger Run & View Results
1. Click **Execute** in the upper right corner of your Test Set page.
2. Select the execution machine (robot) and click **Run**.
3. Once execution is complete, switch to the **Test Results** tab in Test Manager.
4. You will see detailed execution logs:
   * **Status**: `Passed` or `Failed`.
   * **Execution Log**: Step-by-step console logs outputted by your `Log Message` activities.
   * **Screenshots**: If any assertion in the `Verify Expression` activity fails, Test Manager automatically embeds a high-resolution desktop screenshot capturing the error state of the web application.
